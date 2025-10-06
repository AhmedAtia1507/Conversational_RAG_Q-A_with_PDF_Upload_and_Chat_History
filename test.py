from Engines.RAG_Chatbot import RAG_Chatbot

if __name__ == "__main__":
    chatbot = RAG_Chatbot()
    print("Welcome to the chatbot! Please enter the path of the PDF file:")
    pdf_path = input("PDF Path: ")
    chatbot.process_pdf(pdf_path)
    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            print("Chatbot:", end=' ')
            for chunk in chatbot.answer("Ahmed", user_input):
                print(chunk, end='', flush=True)
            print()
    except Exception as e:
        print("Error:", e)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
