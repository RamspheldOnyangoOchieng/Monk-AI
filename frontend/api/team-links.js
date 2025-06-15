import { get, put } from '@vercel/blob';

const BLOB_KEY = 'team-links.json';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    // Fetch the JSON file from Vercel Blob
    try {
      const blob = await get(BLOB_KEY);
      const data = await blob.text();
      res.status(200).json(JSON.parse(data));
    } catch (e) {
      // If not found, return empty array
      res.status(200).json([]);
    }
  } else if (req.method === 'POST') {
    // Update the JSON file in Vercel Blob
    const newMember = req.body;
    let teamLinks = [];
    try {
      const blob = await get(BLOB_KEY);
      teamLinks = JSON.parse(await blob.text());
    } catch (e) {}
    // Replace or add member by unique id (e.g., email or name)
    const idx = teamLinks.findIndex(m => m.email === newMember.email);
    if (idx >= 0) teamLinks[idx] = newMember;
    else teamLinks.push(newMember);
    await put(BLOB_KEY, JSON.stringify(teamLinks), { access: 'public' });
    res.status(200).json({ success: true });
  } else {
    res.status(405).end();
  }
}

export const config = {
  api: {
    bodyParser: true,
  },
}; 