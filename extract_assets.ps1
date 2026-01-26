# Asset extraction script for funsnaps.ca
# Extracts images, contact info, and content from downloaded HTML files

$ErrorActionPreference = "Continue"

# Setup directories
$baseDir = Get-Location
$assetsDir = Join-Path $baseDir "assets\images"
$htmlFiles = Get-ChildItem -Path $baseDir -Filter "*.html"

if ($htmlFiles.Count -eq 0) {
    Write-Host "No HTML files found. Please download HTML files first."
    exit
}

# Create assets directory
New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null

$allImages = @{}
$contactInfo = @{
    phone = @()
    email = @()
    address = @{}
    social_media = @{}
}

foreach ($htmlFile in $htmlFiles) {
    Write-Host "`nProcessing: $($htmlFile.Name)"
    
    $content = Get-Content -Path $htmlFile.FullName -Raw -Encoding UTF8
    
    # Extract images from various sources
    $images = @()
    
    # From img src attributes
    $content | Select-String -Pattern 'src=["'']([^"'']+\.(?:jpg|jpeg|png|gif|webp|svg))' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object { $images += $_.Groups[1].Value }
    }
    
    # From data-src attributes
    $content | Select-String -Pattern 'data-src=["'']([^"'']+\.(?:jpg|jpeg|png|gif|webp|svg))' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object { $images += $_.Groups[1].Value }
    }
    
    # From JSON-LD schema
    $content | Select-String -Pattern '"url":\s*"([^"]+\.(?:jpg|jpeg|png|gif|webp|svg))"' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object { $images += $_.Groups[1].Value }
    }
    $content | Select-String -Pattern '"image":\s*"([^"]+\.(?:jpg|jpeg|png|gif|webp|svg))"' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object { $images += $_.Groups[1].Value }
    }
    $content | Select-String -Pattern '"logo":\s*"([^"]+\.(?:jpg|jpeg|png|gif|webp|svg))"' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object { $images += $_.Groups[1].Value }
    }
    
    # From meta tags
    $content | Select-String -Pattern 'content=["'']([^"'']+\.(?:jpg|jpeg|png|gif|webp|svg))' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object { $images += $_.Groups[1].Value }
    }
    
    # From background-image in style attributes
    $content | Select-String -Pattern 'background-image:\s*url\(["'']?([^"'']+\.(?:jpg|jpeg|png|gif|webp|svg))' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object { $images += $_.Groups[1].Value }
    }
    
    # Filter to funsnaps.ca images only
    foreach ($img in $images) {
        if ($img -match 'funsnaps\.ca' -or $img.StartsWith('/')) {
            if (-not $allImages.ContainsKey($img)) {
                $allImages[$img] = $true
            }
        }
    }
    
    Write-Host "Found $($images.Count) image references"
    
    # Extract contact information
    # Phone numbers
    $content | Select-String -Pattern '(\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object {
            $phone = $_.Value -replace '[^\d+]', ''
            if ($phone -and $contactInfo.phone -notcontains $phone) {
                $contactInfo.phone += $phone
            }
        }
    }
    $content | Select-String -Pattern '"telephone":\s*"([^"]+)"' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object {
            $phone = $_.Groups[1].Value
            if ($phone -and $contactInfo.phone -notcontains $phone) {
                $contactInfo.phone += $phone
            }
        }
    }
    
    # Email addresses
    $content | Select-String -Pattern '([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object {
            $email = $_.Value
            if ($email -and $contactInfo.email -notcontains $email) {
                $contactInfo.email += $email
            }
        }
    }
    
    # Address from JSON-LD
    if ($content -match '"address":\s*\{[^}]+\}') {
        $addrContent = $matches[0]
        if ($addrContent -match '"streetAddress":\s*"([^"]+)"') {
            $contactInfo.address['street'] = $matches[1]
        }
        if ($addrContent -match '"addressLocality":\s*"([^"]+)"') {
            $contactInfo.address['city'] = $matches[1]
        }
        if ($addrContent -match '"addressRegion":\s*"([^"]+)"') {
            $contactInfo.address['region'] = $matches[1]
        }
        if ($addrContent -match '"postalCode":\s*"([^"]+)"') {
            $contactInfo.address['postal_code'] = $matches[1]
        }
        if ($addrContent -match '"addressCountry":\s*"([^"]+)"') {
            $contactInfo.address['country'] = $matches[1]
        }
    }
    
    # Social media
    if ($content -match 'facebook\.com/([^/"'')\s]+)') {
        $contactInfo.social_media['facebook'] = "https://www.facebook.com/$($matches[1])"
    }
    if ($content -match 'instagram\.com/([^/"'')\s]+)') {
        $contactInfo.social_media['instagram'] = "https://www.instagram.com/$($matches[1])"
    }
}

# Save contact info to JSON
$contactJson = @{
    phone = $contactInfo.phone | Select-Object -Unique
    email = $contactInfo.email | Select-Object -Unique
    address = $contactInfo.address
    social_media = $contactInfo.social_media
} | ConvertTo-Json -Depth 10

$contactFile = Join-Path $baseDir "contact_info.json"
$contactJson | Out-File -FilePath $contactFile -Encoding UTF8
Write-Host "`nContact info saved to: $contactFile"

# Download images
Write-Host "`nDownloading $($allImages.Count) images..."
$downloaded = 0
$failed = 0

foreach ($imgUrl in $allImages.Keys) {
    try {
        $url = $imgUrl
        if (-not $url.StartsWith('http')) {
            $url = "https://www.funsnaps.ca$url"
        }
        
        # Parse URL to get path
        $uri = [System.Uri]$url
        $pathParts = $uri.AbsolutePath -split '/'
        
        # Find wp-content in path
        $wpContentIndex = -1
        for ($i = 0; $i -lt $pathParts.Length; $i++) {
            if ($pathParts[$i] -eq 'wp-content') {
                $wpContentIndex = $i
                break
            }
        }
        
        if ($wpContentIndex -ge 0) {
            $relPath = ($pathParts[$wpContentIndex..($pathParts.Length-1)] | Where-Object { $_ }) -join '\'
        } else {
            $relPath = ($pathParts | Where-Object { $_ }) -join '\'
        }
        
        if ($relPath) {
            $outputPath = Join-Path $assetsDir $relPath
            $outputDir = Split-Path $outputPath -Parent
            New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
            
            Write-Host "Downloading: $url"
            Invoke-WebRequest -Uri $url -OutFile $outputPath -ErrorAction Stop
            $downloaded++
        }
    } catch {
        Write-Host "Error downloading $imgUrl : $_" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`nDownloaded $downloaded images to $assetsDir"
if ($failed -gt 0) {
    Write-Host "Failed to download $failed images" -ForegroundColor Yellow
}

# Save image list
$imageListFile = Join-Path $baseDir "image_urls.txt"
$allImages.Keys | Sort-Object | Out-File -FilePath $imageListFile -Encoding UTF8
Write-Host "Image URLs saved to: $imageListFile"





