// File: src/routes/api/job_graph/+server.js

import { json } from '@sveltejs/kit';

/**
 * Handles the POST request to the job_graph endpoint.
 *
 * @param {Object} context - The context object containing the request.
 * @param {Request} context.request - The incoming request object.
 * @returns {Promise<Response>} The response object containing the result of the job graph request.
 * @throws {Error} If there is an error processing the request or the API response.
 */
export async function POST({ request }) {
  try {
    const requestData = await request.json();
    
    // Forward the request to your Python backend
    const response = await fetch('http://localhost:8000/job_graph/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ queries: requestData.queries })
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error: ${errorText}`);
    }
    
    const data = await response.json();
    return json(data);
  } catch (error) {
    console.error('Error in job_graph endpoint:', error);
    return json(
      { error: error instanceof Error ? error.message : 'Unknown error occurred' },
      { status: 500 }
    );
  }
}
