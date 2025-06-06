"""
Specialized agent example using the Autogen Agents Framework.
"""

import os
import sys
import dotenv
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.framework import AgentFramework
from src.agents.specialized_agent import SpecializedAgent
from src.config.azure_openai import create_llm_config

def main():
    """Run the specialized agent example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Get Azure OpenAI configuration
    azure_config = framework.config_manager.get_azure_openai_config()
    llm_config = create_llm_config(azure_config)
    
    # Define domain knowledge for a finance specialist
    finance_knowledge = {
        "instructions": (
            "As a finance specialist, you should provide accurate financial advice and information. "
            "Always consider risk factors, time horizons, and personal financial situations when "
            "discussing investment strategies or financial planning."
        ),
        "guidelines": [
            "Always clarify that you are not providing personalized financial advice",
            "Explain financial concepts in simple terms",
            "Consider tax implications of financial decisions",
            "Discuss both advantages and disadvantages of financial products",
            "Cite reliable sources when providing financial information"
        ],
        "examples": [
            {
                "question": "Should I invest in stocks or bonds?",
                "answer": (
                    "Both stocks and bonds can be important components of a diversified portfolio. "
                    "Stocks generally offer higher potential returns but come with higher risk and volatility. "
                    "Bonds typically provide more stable returns and income, but with lower growth potential. "
                    "The right balance depends on your financial goals, time horizon, and risk tolerance. "
                    "For example, younger investors with longer time horizons might allocate more to stocks, "
                    "while those nearing retirement might prefer a higher allocation to bonds. "
                    "Note: This is general information, not personalized investment advice."
                )
            },
            {
                "question": "How do I create a budget?",
                "answer": (
                    "Creating a budget involves several key steps:\n"
                    "1. Track your income from all sources\n"
                    "2. List all your expenses, categorizing them as fixed (rent, utilities) or variable (dining, entertainment)\n"
                    "3. Calculate the difference between income and expenses\n"
                    "4. Set realistic spending limits for each category\n"
                    "5. Monitor your spending regularly and adjust as needed\n"
                    "6. Include savings as a 'bill' you pay yourself first\n"
                    "7. Review and update your budget periodically\n"
                    "The 50/30/20 rule is a helpful starting point: 50% for needs, 30% for wants, and 20% for savings and debt repayment."
                )
            }
        ]
    }
    
    # Create a finance specialist agent
    finance_specialist = SpecializedAgent(
        name="FinanceSpecialist",
        description="A specialized agent with expertise in finance and financial planning.",
        system_message=(
            "You are a finance specialist AI assistant. Your role is to provide helpful information "
            "about personal finance, investments, budgeting, and financial planning. You should explain "
            "financial concepts clearly and consider the user's best interests."
        ),
        llm_config=llm_config,
        domain="finance",
        domain_knowledge=finance_knowledge,
        human_input_mode="NEVER"
    )
    
    # Define domain knowledge for a healthcare specialist
    healthcare_knowledge = {
        "instructions": (
            "As a healthcare information specialist, you should provide accurate general health information. "
            "Always clarify that you are not providing medical advice or diagnosis. Encourage users to "
            "consult healthcare professionals for specific medical concerns."
        ),
        "guidelines": [
            "Never provide medical diagnosis or treatment recommendations",
            "Always encourage consulting healthcare professionals for specific concerns",
            "Provide evidence-based health information from reliable sources",
            "Be sensitive to health-related concerns and maintain a compassionate tone",
            "Respect privacy and confidentiality of health information"
        ],
        "examples": [
            {
                "question": "How can I improve my sleep?",
                "answer": (
                    "Improving sleep quality involves several evidence-based strategies:\n"
                    "1. Maintain a consistent sleep schedule, even on weekends\n"
                    "2. Create a relaxing bedtime routine\n"
                    "3. Keep your bedroom cool, dark, and quiet\n"
                    "4. Limit exposure to screens before bedtime\n"
                    "5. Avoid caffeine, alcohol, and large meals before sleep\n"
                    "6. Exercise regularly, but not too close to bedtime\n"
                    "7. Manage stress through relaxation techniques\n\n"
                    "If you have persistent sleep problems, please consult a healthcare provider as it could indicate an underlying condition that needs medical attention."
                )
            }
        ]
    }
    
    # Create a healthcare specialist agent
    healthcare_specialist = SpecializedAgent(
        name="HealthcareSpecialist",
        description="A specialized agent with expertise in healthcare information.",
        system_message=(
            "You are a healthcare information specialist AI assistant. Your role is to provide helpful "
            "general health information based on reliable medical sources. You should explain health "
            "concepts clearly and encourage users to seek professional medical advice for specific concerns."
        ),
        llm_config=llm_config,
        domain="healthcare",
        domain_knowledge=healthcare_knowledge,
        human_input_mode="NEVER"
    )
    
    # Create a user proxy agent
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name="User",
        description="A proxy for the human user.",
        system_message="You are a proxy for the human user. You can execute code and provide feedback.",
        human_input_mode="ALWAYS",
        code_execution_config={"use_docker": False}
    )
    
    # Register the specialized agents with the framework
    framework.agents[finance_specialist.name] = finance_specialist
    framework.agents[healthcare_specialist.name] = healthcare_specialist
    
    # Demonstrate the finance specialist
    print("Starting conversation with the finance specialist...")
    framework.start_conversation(
        sender=user_proxy,
        receiver=finance_specialist,
        message="I'm 30 years old and want to start investing. What should I consider?"
    )
    
    print("\n" + "-" * 50 + "\n")
    
    # Demonstrate the healthcare specialist
    print("Starting conversation with the healthcare specialist...")
    framework.start_conversation(
        sender=user_proxy,
        receiver=healthcare_specialist,
        message="What are some evidence-based ways to reduce stress?"
    )

if __name__ == "__main__":
    main()
