import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  try {
    const jobNames = await request.json();
    
    // Forward the request to your Python backend
    const response = await fetch('http://localhost:8000/skill_graph/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jobNames)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error: ${errorText}`);
    }
    
    const data = await response.json();
    return json(data);
  } catch (error) {
    console.error('Error in skill_graph endpoint:', error);
    return json(
      { error: error instanceof Error ? error.message : 'Unknown error occurred' },
      { status: 500 }
    );
  }
}
