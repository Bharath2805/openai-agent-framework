import gradio as gr
# Try the simple version first, fallback to complex if needed
try:
    from simple_research_assistant import SimpleResearchAssistant as ResearchAssistant
    print("Using Simple Research Assistant (recursion-safe)")
except:
    from research_assistant import ResearchAssistant
    print("Using Full Research Assistant")
import asyncio

async def setup_research_assistant():
    """Initialize the research assistant"""
    assistant = ResearchAssistant()
    await assistant.setup()
    return assistant

async def process_research_request(assistant, research_topic, quality_criteria, history):
    """Process a research request"""
    try:
        results = await assistant.conduct_research(research_topic, quality_criteria, history)
        return results, assistant
    except Exception as e:
        error_msg = {"role": "assistant", "content": f"❌ Error during research: {str(e)}"}
        return history + [error_msg], assistant
    
async def reset_assistant():
    """Reset and create a new research assistant"""
    new_assistant = ResearchAssistant()
    await new_assistant.setup()
    return "", "", None, new_assistant

def cleanup_resources(assistant):
    """Clean up assistant resources"""
    print("🧹 Cleaning up research assistant resources...")
    try:
        if assistant:
            assistant.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")

with gr.Blocks(
    title="🔬 Research Assistant", 
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="purple")
) as app:
    
    gr.HTML("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
        <h1>🔬 AI Research Assistant</h1>
        <p>Your intelligent companion for comprehensive research and analysis</p>
    </div>
    """)
    
    assistant = gr.State(delete_callback=cleanup_resources)
    
    # Main chat interface
    chatbot = gr.Chatbot(
        label="Research Session",
        height=500,
        type="messages",
        placeholder="Your research session will appear here...",
        show_copy_button=True
    )
    
    # Examples in a collapsible section
    with gr.Accordion("📚 Examples & Tips", open=True):
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                ### 📚 Example Research Topics:
                - AI impact on education systems
                - Sustainable energy for developing countries  
                - Social media psychology effects
                - Blockchain in healthcare
                - Climate change & agriculture
                - Remote work productivity studies
                - Electric vehicle adoption trends
                """)
            
            with gr.Column():
                gr.Markdown("""
                ### ⭐ Quality Criteria Examples:
                - Academic-level with 5+ credible sources
                - Current statistics & real-world examples
                - In-depth analysis with case studies
                - Technical implementation details
                - Policy recommendations included
                - Expert opinions and interviews
                - Comparative analysis across regions
                """)
    
    with gr.Group():
        with gr.Row():
            research_topic = gr.Textbox(
                label="🎯 Research Topic",
                placeholder="Enter your research topic or question...",
                lines=2,
                scale=2
            )
        
        with gr.Row():
            quality_criteria = gr.Textbox(
                label="📋 Quality Criteria & Requirements",
                placeholder="Specify your quality requirements (depth, sources, format, etc.)",
                lines=2,
                scale=2
            )
    
    with gr.Row():
        reset_btn = gr.Button("🔄 New Research Session", variant="secondary")
        research_btn = gr.Button("🚀 Start Research", variant="primary", size="lg")
    
    gr.Markdown("""
    ### 📱 WhatsApp Notifications
    You'll receive WhatsApp updates when research milestones are completed!
    
    ### 📁 File Outputs
    Research results are automatically saved to the `research_outputs/` directory.
    
    ### 🔍 Research Process
    1. **Search** - Multiple sources including web and Wikipedia
    2. **Analysis** - AI evaluates and synthesizes information  
    3. **Quality Check** - Ensures research meets your criteria
    4. **Notification** - WhatsApp alert when complete
    """)
    
    # Event handlers
    app.load(setup_research_assistant, [], [assistant])
    
    research_topic.submit(
        process_research_request, 
        [assistant, research_topic, quality_criteria, chatbot], 
        [chatbot, assistant]
    )
    
    quality_criteria.submit(
        process_research_request, 
        [assistant, research_topic, quality_criteria, chatbot], 
        [chatbot, assistant]
    )
    
    research_btn.click(
        process_research_request, 
        [assistant, research_topic, quality_criteria, chatbot], 
        [chatbot, assistant]
    )
    
    reset_btn.click(
        reset_assistant, 
        [], 
        [research_topic, quality_criteria, chatbot, assistant]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        share=False
    )