<script lang="ts">
  import { onMount } from 'svelte';
  import ForceGraph from '../lib/ForceGraph.svelte';
  import BaseGraph from '../lib/BaseGraph.svelte';
  import { type Node, type Edge } from '@xyflow/svelte';
  import { writable } from 'svelte/store';


  const xPosInterval = 200;
  const yPosInterval = 200;

  let nlQuery = '';
  let isLoading = false;
  // let graphData = { nodes: [], edges: [] };
  let graphData: JobGraphResponse;
  let nodes= writable<Node[]>([]);
  let edges = writable<Edge[]>([]);

  /**
 * @type {Error|null} error - Holds the error object if an error occurs, otherwise null.
 */
  let error: Error | null = null;
  
  type APINode = {
    job: string;
    min_salary: number;
    max_salary: number;
    min_exp: number;
    max_exp: number;
    level: string;
    category: string;
    job_description: string;
    hard_skill: string[];
    soft_skill: string[];
    interest: string[];
    education: string[];
  };

  type JobGraphResponse = {
    nlq: string;
    user_input: {
      hard_skill: string[];
      soft_skill: string[];
      interest: string[];
      education: string[];
    }
    nodes: (APINode & {children: APINode[]})[];
  };

  async function generateJobGraph() {
    if (!nlQuery.trim()) {
      error = new Error("Please enter a natural language query");
      return;
    }
    
    error = null;
    isLoading = true;
    
    try {
      graphData = {
    "nlq": "I have pyton skill, leadership, communicate and I love playing games. What job match me with some of my skill?",
    "user_input": {
        "hard_skill": [
            "Python"
        ],
        "soft_skill": [
            "Leadership",
            "Communication"
        ],
        "interest": [
            "Game Design"
        ],
        "education": []
    },
    "nodes": [
        {
            "job": "Junior Software Engineer",
            "min_salary": 30000,
            "max_salary": 50000,
            "min_exp": 1,
            "max_exp": 3,
            "level": "Junior",
            "category": "Technology",
            "job_description": "A Junior Software Engineer designs, develops, and maintains software applications under the guidance of senior engineers. Responsibilities include writing code in languages such as Python, Java, or JavaScript, debugging software, participating in code reviews, and testing features to ensure functionality and performance. The role involves learning and applying best practices in software development, collaborating with teams, and using version control systems like Git. Ideal for entry-level professionals with 0-2 years of experience or relevant internships.",
            "hard_skill": [
                "CSS",
                "HTML",
                "Python",
                "Git",
                "JavaScript"
            ],
            "soft_skill": [
                "Communication",
                "Adaptability",
                "Time Management",
                "Problem Solving",
                "Team Leadership"
            ],
            "interest": [
                "Web Development",
                "Technology",
                "Mobile Apps",
                "AI",
                "Mobile Gaming"
            ],
            "education": [
                "Bachelor's in Computer Science",
                "Bachelor's in Software Engineering"
            ],
            "children": [
                {
                    "job": "Full Stack Developer",
                    "min_salary": 60000,
                    "max_salary": 90000,
                    "min_exp": 3,
                    "max_exp": 7,
                    "level": "Mid",
                    "category": "Technology",
                    "job_description": "A Full Stack Developer works on both frontend and backend development to create end-to-end web solutions. Responsibilities include designing user interfaces with HTML, CSS, and JavaScript, building APIs with Python or Node.js, and managing databases. The role requires 3+ years of experience, versatility in web technologies, and problem-solving skills.",
                    "hard_skill": [
                        "CSS",
                        "Node.js",
                        "MongoDB",
                        "HTML",
                        "React",
                        "JavaScript"
                    ],
                    "soft_skill": [
                        "Communication",
                        "Attention to Detail",
                        "Adaptability",
                        "Time Management",
                        "Problem Solving",
                        "Team Leadership"
                    ],
                    "interest": [
                        "User Experience",
                        "Web Development",
                        "System Architecture",
                        "Database Design"
                    ],
                    "education": [
                        "Bachelor's in Computer Science",
                        "Bachelor's in Software Engineering",
                        "Bachelor's in Web Development"
                    ]
                },
                {
                    "job": "Frontend Developer",
                    "min_salary": 50000,
                    "max_salary": 80000,
                    "min_exp": 2,
                    "max_exp": 5,
                    "level": "Mid",
                    "category": "Technology",
                    "job_description": "A Frontend Developer builds user interfaces for web applications, focusing on responsive, visually appealing, and functional designs. Responsibilities include writing clean code in HTML, CSS, and JavaScript, ensuring cross-browser compatibility, and collaborating with backend developers using frameworks like React or Angular. The role requires 2+ years of experience and knowledge of modern web technologies and UX trends.",
                    "hard_skill": [
                        "CSS",
                        "HTML",
                        "React",
                        "JavaScript",
                        "Vue.js",
                        "Responsive Design"
                    ],
                    "soft_skill": [
                        "Communication",
                        "Attention to Detail",
                        "Creativity",
                        "Problem Solving",
                        "Team Leadership"
                    ],
                    "interest": [
                        "Web Development",
                        "Design Systems",
                        "Web Animation",
                        "User Interface"
                    ],
                    "education": [
                        "Associate's in Web Design",
                        "Bachelor's in Computer Science",
                        "Bachelor's in Web Development"
                    ]
                }
            ]
        },
        {
            "job": "Quality Assurance Engineer",
            "min_salary": 45000,
            "max_salary": 75000,
            "min_exp": 2,
            "max_exp": 5,
            "level": "Mid",
            "category": "Technology",
            "job_description": "A Quality Assurance Engineer tests software applications to ensure they meet quality and functional requirements. Responsibilities include designing test plans, executing manual/automated tests, reporting bugs, and collaborating with developers using tools like Selenium or JIRA. The role requires 2+ years of experience and knowledge of testing methodologies.",
            "hard_skill": [
                "Penetration Testing",
                "Usability Testing",
                "Jira",
                "Python",
                "Analytics"
            ],
            "soft_skill": [
                "Communication",
                "Attention to Detail",
                "Problem Solving",
                "Analytical Thinking",
                "Critical Thinking",
                "Patience"
            ],
            "interest": [
                "Process Improvement",
                "Software Quality",
                "Automation",
                "User Experience",
                "Customer Service"
            ],
            "education": [
                "Bachelor's in Information Technology",
                "Bachelor's in Computer Science",
                "Bachelor's in Software Engineering"
            ],
            "children": [
                {
                    "job": "Software Quality Assurance Engineer",
                    "min_salary": 55000,
                    "max_salary": 85000,
                    "min_exp": 2,
                    "max_exp": 6,
                    "level": "Mid",
                    "category": "Technology",
                    "job_description": "A Software Quality Assurance Engineer tests software to ensure it meets quality and functional requirements. Responsibilities include designing test plans, executing tests, and reporting bugs using tools like Selenium or JIRA. The role requires 2+ years of experience, a degree in IT or engineering, and knowledge of testing methodologies.",
                    "hard_skill": [
                        "Penetration Testing",
                        "Usability Testing",
                        "Performance Management",
                        "Anomaly Detection",
                        "Security Automation",
                        "Quality Control"
                    ],
                    "soft_skill": [
                        "Communication",
                        "Attention to Detail",
                        "Technical Understanding",
                        "Problem Solving",
                        "Analytical Thinking",
                        "Critical Thinking",
                        "Organization"
                    ],
                    "interest": [
                        "Software Quality",
                        "Software Development",
                        "Automation"
                    ],
                    "education": [
                        "Bachelor's in Accounting",
                        "Bachelor's in Computer Science",
                        "Bachelor's in Software Engineering"
                    ]
                },
                {
                    "job": "Computational Linguist",
                    "min_salary": 70000,
                    "max_salary": 105000,
                    "min_exp": 4,
                    "max_exp": 8,
                    "level": "Senior",
                    "category": "Technology",
                    "job_description": "A Computational Linguist develops language-processing systems using computational methods, such as chatbots or translation tools. Responsibilities include building models, analyzing linguistic data, and integrating solutions using Python and NLP frameworks. The role requires 3+ years of experience, a degree in linguistics or computer science, and expertise in NLP.",
                    "hard_skill": [
                        "NLP",
                        "Data Modeling",
                        "Python",
                        "Natural Language Processing",
                        "Machine Learning",
                        "Analytics"
                    ],
                    "soft_skill": [
                        "Communication",
                        "Attention to Detail",
                        "Technical Understanding",
                        "Critical Thinking",
                        "Problem Solving",
                        "Analytical Thinking",
                        "Research"
                    ],
                    "interest": [
                        "AI",
                        "Computational Linguistics",
                        "Technology"
                    ],
                    "education": [
                        "Master's in Linguistics",
                        "PhD in Linguistics",
                        "Master's in Computer Science"
                    ]
                }
            ]
        },
        {
            "job": "AI Engineer",
            "min_salary": 60000,
            "max_salary": 100000,
            "min_exp": 3,
            "max_exp": 7,
            "level": "Mid",
            "category": "Technology",
            "job_description": "An AI Engineer develops and implements artificial intelligence and machine learning solutions to address business challenges. Responsibilities include designing algorithms, training models using frameworks like TensorFlow or PyTorch, integrating AI into products, and optimizing performance for tasks like natural language processing or computer vision. The role requires collaboration with data scientists and engineers, a strong background in AI/ML, and 3+ years of experience in Python-based development.",
            "hard_skill": [
                "NLP",
                "TensorFlow",
                "Python",
                "PyTorch",
                "Machine Learning",
                "Computer Vision"
            ],
            "soft_skill": [
                "Communication",
                "Adaptability",
                "Problem Solving",
                "Analytical Thinking",
                "Research"
            ],
            "interest": [
                "Research",
                "Data Science",
                "AI",
                "Deep Learning",
                "Robotics"
            ],
            "education": [
                "Master's in Artificial Intelligence",
                "Bachelor's in Data Science",
                "Bachelor's in Computer Science"
            ],
            "children": [
                {
                    "job": "Computer Vision Engineer",
                    "min_salary": 75000,
                    "max_salary": 115000,
                    "min_exp": 4,
                    "max_exp": 8,
                    "level": "Senior",
                    "category": "Technology",
                    "job_description": "A Computer Vision Engineer develops systems that interpret visual data, such as facial recognition or autonomous vehicles. Responsibilities include building models, integrating with cameras, and optimizing performance using Python, OpenCV, and TensorFlow. The role requires 3+ years of experience, expertise in computer vision, and machine learning knowledge.",
                    "hard_skill": [
                        "Image Recognition",
                        "Python",
                        "Neural Networks",
                        "Video Editing",
                        "Machine Learning",
                        "Computer Vision"
                    ],
                    "soft_skill": [
                        "Communication",
                        "Attention to Detail",
                        "Technical Understanding",
                        "Critical Thinking",
                        "Problem Solving",
                        "Analytical Thinking",
                        "Research"
                    ],
                    "interest": [
                        "AI",
                        "Computer Vision",
                        "Robotics",
                        "Machine Learning"
                    ],
                    "education": [
                        "Master's in Machine Learning",
                        "PhD in Computer Science",
                        "Bachelor's in Computer Science"
                    ]
                },
                {
                    "job": "Machine Learning Engineer",
                    "min_salary": 80000,
                    "max_salary": 120000,
                    "min_exp": 4,
                    "max_exp": 8,
                    "level": "Senior",
                    "category": "Technology",
                    "job_description": "A Machine Learning Engineer develops and deploys machine learning models to solve business problems. Responsibilities include data preprocessing, model training with frameworks like TensorFlow, and integrating solutions into products. The role requires 3+ years of experience, expertise in Python, and knowledge of AI/ML algorithms.",
                    "hard_skill": [
                        "TensorFlow",
                        "Python",
                        "Data Preprocessing",
                        "Model Deployment",
                        "Deep Learning",
                        "PyTorch"
                    ],
                    "soft_skill": [
                        "Communication",
                        "Attention to Detail",
                        "Critical Thinking",
                        "Creativity",
                        "Problem Solving",
                        "Analytical Thinking",
                        "Research"
                    ],
                    "interest": [
                        "Neural Networks",
                        "Data Science",
                        "Machine Learning",
                        "Algorithm Design",
                        "AI"
                    ],
                    "education": [
                        "Master's in Machine Learning",
                        "PhD in Data Science",
                        "Bachelor's in Computer Science"
                    ]
                }
            ]
        }
    ]
}
      // const response = await fetch('/api/job_graph', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json'
      //   },
      //   body: JSON.stringify({ queries: [nlQuery] })
      // });
      
      // if (!response.ok) {
      //   throw new Error('Failed to generate job graph');
      // }
      
      // graphData = await response.json();

      const { mappedNodes, mappedEdges } = mapAPINodesToNodesAndEdges(graphData)

      // Additional start position that is not a job node
      mappedNodes.push({
        id:   "start-node",
        type: 'input',
        data: {label: 'start'},
        position: {x: xPosInterval*2, y: 0},
      });

      nodes.set(mappedNodes)
      edges.set(mappedEdges)

    } catch (err) {
      error = (err instanceof Error) ? err : new Error('An unknown error occurred');
      console.error('Error generating job graph:', err);
    } finally {
      isLoading = false;
    }
  }

  // Node
  // {
  //     id: '1',
  //     type: 'input',
  //     data: { label: 'Start' },
  //     position: { x: 200, y: 0 }
  //   },

  // Edge
  // {
  //     id: '1-2',
  //     source: '1',
  //     target: '2',
  //   },

  function mapAPINodesToNodesAndEdges(response: JobGraphResponse): {mappedNodes: Node[], mappedEdges: Edge[]} {
    const mappedNodes: Node[] = [];
    const mappedEdges: Edge[] = [];

    response?.nodes?.forEach((node, i) => {
      // First layer of nodes
      mappedNodes.push({
        id:   node.job, // current data set has unique job name, so it can be an id for now
        // type: 'input',
        data: {label: node.job},
        position: {x: i * (xPosInterval * 2), y: yPosInterval},
      });

      mappedEdges.push({
        id: `start-node-${node.job}`,
        source: 'start-node',
        target: node.job,
      });

      // Since there will only be maximum 2 layers, no need for recursion here.
      // 2nd layer of nodes
      node?.children?.forEach((child, j) => {
        mappedNodes.push({
          id:   child.job,
          type: 'output',
          data: {label: child.job},
          position: {x: (i * xPosInterval * 2 + (j * xPosInterval)), y: yPosInterval * 2},
        });

        mappedEdges.push({
          id: `${node.job}-${child.job}`,
          source: node.job,
          target: child.job,
        });
      })
    });

    // for (let i = 0; i < response?.nodes.length; i++) {
    //   const node = response?.nodes[i];

    //   // First layer of nodes
    //   nodes.push({
    //     id:   node.job, // current data set has unique job name, so it can be an id for now
    //     type: 'input',
    //     data: {label: node.job},
    //     position: {x: 0, y: 0},
    //   });

    //   // Since there will only be maximum 2 layers, no need for recursion here.
    //   // 2nd layer of nodes
    //   for (const child of node.children) {
    //     nodes.push({
    //       id:   child.job,
    //       type: 'input',
    //       data: {label: child.job},
    //       position: {x: 0, y: 0},
    //     });
    //   }
    // }

    return {mappedNodes, mappedEdges};
  }


</script>

<main class="min-h-full bg-stone-100 p-8">
  <!-- <h2 class="text-xl font-bold text-blue-500 mb-4">Jobs Graph</h2> -->
  
  <section class="min-h-full rounded-md mb-8">
    <!-- <h3 class="text-center text-gray-700 mb-2">NLQ &lt;input&gt;</h3> -->
    <h2 class="text-center font-medium text-stone-700 mb-2">Tell us what you're interested in</h2>
    <div class="flex gap-2">
      <textarea 
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
      ></textarea>
      <!-- <input
        type="text"
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border rounded-md text-stone-800 placeholder-stone-300"
      /> -->
      <button 
        on:click={generateJobGraph}
        disabled={isLoading}
        class="bg-lime-600 text-stone-50 px-4 py-2 rounded-md hover:bg-lime-700 disabled:bg-stone-400"
      >
        {isLoading ? 'Loading...' : 'Generate'}
      </button>
    </div>
    {#if error}
      <p class="text-red-500 mt-2">{error}</p>
    {/if}
  </section>
  
  <section class="h-[70vh] rounded-md">
    <!-- <h3 class="text-center text-gray-700">JOBS GRAPH &lt;output&gt;</h3> -->
    <h3 class="text-center font-medium text-stone-700 mb-2">Job Matches Based on Your Interests & Skills</h3>
    <!-- <div class="graph-container min-h-[75vh] outline-2 outline-red-600 bg-stone-100 rounded-md border"> -->
    <BaseGraph {nodes} {edges} />
      <!-- {#if graphData.nodes.length > 0}
        <ForceGraph {graphData} />
      {:else}
        <div class="flex items-center justify-center h-full text-gray-400">
          Enter a query and click Generate to see the job graph
        </div>
      {/if} -->
    <!-- </div> -->
  </section>
</main>