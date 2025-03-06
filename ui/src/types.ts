export type APINode = {
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

export type JobGraphResponse = {
  nlq: string;
  user_input: {
    hard_skill: string[];
    soft_skill: string[];
    interest: string[];
    education: string[];
  };
  nodes: (APINode & { children: APINode[] })[];
};
