import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, phone, 'event-date': eventDate, 'event-type': eventType, message } = req.body;

    // Validate required fields
    if (!name || !email || !phone) {
      return res.status(400).json({ error: 'Name, email, and phone are required' });
    }

    // Format the email content
    const emailContent = `
      <h2>New Contact Form Submission</h2>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Phone:</strong> ${phone}</p>
      ${eventDate ? `<p><strong>Event Date:</strong> ${eventDate}</p>` : ''}
      ${eventType ? `<p><strong>Event Type:</strong> ${eventType}</p>` : ''}
      ${message ? `<p><strong>Message:</strong><br>${message.replace(/\n/g, '<br>')}</p>` : ''}
    `;

    // Send email using Resend
    const data = await resend.emails.send({
      from: process.env.RESEND_FROM_EMAIL || 'Fun Snaps <onboarding@resend.dev>',
      to: process.env.RESEND_TO_EMAIL || 'info@funsnaps.ca',
      replyTo: email,
      subject: `New Contact Form Submission from ${name}`,
      html: emailContent,
    });

    return res.status(200).json({ success: true, message: 'Email sent successfully', data });
  } catch (error) {
    console.error('Error sending email:', error);
    return res.status(500).json({ error: 'Failed to send email', details: error.message });
  }
}
