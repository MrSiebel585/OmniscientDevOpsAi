# omniscient_ai_pipeline/main.py

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFacePipeline
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os, logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
os.makedirs("logs", exist_ok=True)

# ========== CONFIG ==========
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"  # swap with Llama or Starcoder if needed

# ========== LLM WRAPPER ==========
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
model = AutoModelForCausalLM.from_pretrained(HF_MODEL, device_map="auto")
generation_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=generation_pipeline)

# ========== MEMORY ==========
memory = ConversationBufferMemory(memory_key="chat_history")

# ========== TASK PLANNER ==========
task_prompt = PromptTemplate(
    input_variables=["input"],
    template="""
    You are the development planner for an advanced AI system called Omniscient.
    Break down the following user task into a JSON list of subtasks with clear descriptions:

    Task: {input}
    """
)
planner_chain = LLMChain(llm=llm, prompt=task_prompt, memory=memory)

# ========== TOOLS ==========
def task_planner_tool(task: str):
    logging.info("Planning tasks...")
    return planner_chain.run(task)

tools = [
    Tool(
        name="TaskPlanner",
        func=task_planner_tool,
        description="Breaks down development tasks into sub-tasks"
    )
]

# ========== AGENT INITIALIZATION ==========
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    memory=memory
)

# ========== MAIN INTERFACE ==========
def main():
    print("👁️ Omniscient DevOps AI Pipeline Loaded")
    while True:
        user_input = input("\n🧠 Ask Omniscient to develop something (or type 'exit'): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run(user_input)
        print("\n📋 Result:")
        print(response)
        with open("logs/dev_session.log", "a") as f:
            f.write(f"\n\nUSER: {user_input}\nAI: {response}\n")

if __name__ == "__main__":
    main()
