import { Component, OnInit } from '@angular/core';
import { ChatbotService } from '../../service/chatbot.service';

interface Message {
  text: string;
  isUser: boolean;
  isHtml?: boolean;  // Add a flag to check if the content is HTML
}

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  
  isProfileVisible: boolean = false;
  isDiscordWindowVisible: boolean = false;
  isPopupVisible: boolean = false;

  message: string = '';  // Holds the current input message
  messages: Array<{ type: string, text: string, isHtml?: boolean }> = []; // Array to hold chat messages

  selectedFile: File | null = null;
  question: string = '';
  response: string = '';
  error: string = '';

  constructor(private documentService: ChatbotService) { }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  onSubmit() {
    if (this.selectedFile && this.question) {
      this.messages.push({ type: 'user', text: this.question });
      console.log(this.selectedFile, this.question)
      this.documentService.uploadDocument(this.selectedFile, this.question)
        .subscribe(
          (data) => {
            this.response = data.answer;
            this.messages.push({ type: 'bot', text: this.response, isHtml: true });
            this.error = '';
          },
          (err) => {
            if (err.error && err.error.error) {
              this.error = err.error.error;
              this.messages.push({ type: 'bot', text: this.error });
            } else {
              this.error = 'An unexpected error occurred. Please try again later.';
              this.messages.push({ type: 'bot', text: this.error });
            }
            this.response = '';
          }
        );
    } else {
      this.messages.push({ type: 'user', text: this.question });
      this.error = 'Please select a file and enter a question.';
      this.messages.push({ type: 'bot', text: this.error });
    }
    this.question = '';
  }
  
  // Function to send the message
  sendMessage() {
    if (this.message.trim()) {
      // Push user message to the messages array
      this.messages.push({ type: 'user', text: this.message });

      // Clear the input field
      this.message = '';

      // Simulate bot response (you can customize the response)
      setTimeout(() => {
        this.messages.push({ type: 'bot', text: 'Thank you for your message!' });
      }, 1000);
    }
  }

  // Function to listen for the Enter key
  onEnterPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      this.onSubmit();
    }
  }

  // Toggles the visibility of the popup window
  togglePopup() {
    this.isPopupVisible = !this.isPopupVisible;
  }

  // Methods for the popup options
  doAction1() {
    console.log('Option 1 selected');
    this.isPopupVisible = false; // Close the popup after selecting an option
  }

  doAction2() {
    console.log('Option 2 selected');
    this.isPopupVisible = false;
  }

  doAction3() {
    console.log('Option 3 selected');
    this.isPopupVisible = false;
  }

  showProfile(): void {
    this.isProfileVisible = true;
    this.isDiscordWindowVisible = false

  }
  showDiscordWindow(): void {
    this.isDiscordWindowVisible = true
    this.isProfileVisible = false;

  }

  openSettings() {
    console.log('Settings icon clicked!');
    // Logic for opening settings or performing any action
  }
  
}
