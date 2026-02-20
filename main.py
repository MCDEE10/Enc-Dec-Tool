"""
Main CLI application for Text Encryption & Decryption Tool
"""

from encryption import EncryptionManager
from file_handler import FileHandler
import os
import sys

class TextEncryptionTool:
    def __init__(self):
        self.encryptor = EncryptionManager()
        self.file_handler = FileHandler()
        self.current_method = "fernet"  # Default method
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("=" * 60)
        print("           TEXT ENCRYPTION & DECRYPTION TOOL")
        print("=" * 60)
    
    def print_menu(self):
        """Print main menu"""
        print("\nMAIN MENU:")
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Switch Encryption Method")
        print("4. Key Management")
        print("5. File Operations")
        print("6. Exit")
        print("-" * 60)
    
    def encrypt_text_menu(self):
        """Handle text encryption"""
        self.clear_screen()
        self.print_header()
        print("\n--- ENCRYPT TEXT ---")
        
        # Get user input
        text = input("\nEnter text to encrypt: ")
        
        if not text:
            print("No text entered!")
            return
        
        result = None
        key_info = ""
        
        if self.current_method == "caesar":
            shift = input("Enter shift value (default 3): ")
            shift = int(shift) if shift.strip() else 3
            result = self.encryptor.caesar_encrypt(text, shift)
            key_info = f"Shift: {shift}"
        
        elif self.current_method == "fernet":
            # Generate new key for each encryption if not exists
            if not self.encryptor.current_key:
                key = self.encryptor.generate_key()
                print(f"\n🔑 New Key Generated: {key.decode('utf-8')}")
                print("⚠️  SAVE THIS KEY - You'll need it for decryption!")
            
            result = self.encryptor.fernet_encrypt(text)
            key_info = f"Key: {self.encryptor.get_key_string()}"
        
        print(f"\n✅ Encrypted Text:\n{result}")
        print(f"\nℹ️  {key_info}")
        
        # Ask to save to file
        save = input("\nSave to file? (y/n): ").lower()
        if save == 'y':
            filename = self.file_handler.save_encrypted_text(
                result, 
                self.current_method
            )
            print(f"✅ Saved to: {filename}")
    
    def decrypt_text_menu(self):
        """Handle text decryption"""
        self.clear_screen()
        self.print_header()
        print("\n--- DECRYPT TEXT ---")
        
        print("\nOptions:")
        print("1. Enter text directly")
        print("2. Load from file")
        choice = input("Choose (1/2): ")
        
        encrypted_text = None
        
        if choice == '1':
            encrypted_text = input("\nEnter encrypted text: ")
        elif choice == '2':
            # Show available files
            files = self.file_handler.list_encrypted_files()
            if not files:
                print("No encrypted files found!")
                return
            
            print("\nAvailable files:")
            for i, f in enumerate(files, 1):
                print(f"{i}. {f}")
            
            file_choice = input("\nSelect file number: ")
            try:
                idx = int(file_choice) - 1
                filename = f"{self.file_handler.default_dir}/{files[idx]}"
                encrypted_text = self.file_handler.load_encrypted_text(filename)
                print(f"Loaded text from: {filename}")
            except (ValueError, IndexError):
                print("Invalid selection!")
                return
        else:
            return
        
        if not encrypted_text:
            print("No text to decrypt!")
            return
        
        result = None
        
        if self.current_method == "caesar":
            shift = input("Enter shift value used for encryption: ")
            try:
                shift = int(shift)
                result = self.encryptor.caesar_decrypt(encrypted_text, shift)
            except ValueError:
                print("Invalid shift value!")
                return
        
        elif self.current_method == "fernet":
            # Check if key is loaded
            if not self.encryptor.current_key:
                key_input = input("Enter the decryption key: ")
                try:
                    self.encryptor.load_key(key_input)
                except Exception:
                    print("Invalid key format!")
                    return
            
            try:
                result = self.encryptor.fernet_decrypt(encrypted_text)
            except Exception as e:
                print(f"Decryption failed: {e}")
                return
        
        print(f"\n✅ Decrypted Text:\n{result}")
    
    def switch_method_menu(self):
        """Switch between encryption methods"""
        self.clear_screen()
        self.print_header()
        print("\n--- ENCRYPTION METHODS ---")
        print(f"Current method: {self.current_method.upper()}")
        print("\nAvailable methods:")
        print("1. Caesar Cipher (basic)")
        print("2. Fernet (strong encryption)")
        
        choice = input("\nSelect method (1/2): ")
        
        if choice == '1':
            self.current_method = "caesar"
            print("✅ Switched to Caesar Cipher")
        elif choice == '2':
            self.current_method = "fernet"
            # Generate new key for Fernet
            key = self.encryptor.generate_key()
            print(f"✅ Switched to Fernet Encryption")
            print(f"🔑 New Key: {key.decode('utf-8')}")
            print("⚠️  SAVE THIS KEY!")
        else:
            print("Invalid choice!")
    
    def key_management_menu(self):
        """Handle key management operations"""
        self.clear_screen()
        self.print_header()
        print("\n--- KEY MANAGEMENT ---")
        print(f"Current method: {self.current_method.upper()}")
        
        if self.current_method == "caesar":
            print("\nCaesar cipher doesn't use keys. Use shift values instead.")
            return
        
        print("\nOptions:")
        print("1. Generate new key")
        print("2. Show current key")
        print("3. Save key to file")
        print("4. Load key from file")
        print("5. Load key manually")
        
        choice = input("\nSelect option: ")
        
        if choice == '1':
            key = self.encryptor.generate_key()
            print(f"✅ New key generated: {key.decode('utf-8')}")
            print("⚠️  SAVE THIS KEY!")
        
        elif choice == '2':
            key = self.encryptor.get_key_string()
            if key:
                print(f"🔑 Current key: {key}")
            else:
                print("No key loaded!")
        
        elif choice == '3':
            if self.encryptor.current_key:
                filename = input("Enter filename to save (default: secret.key): ")
                if not filename:
                    filename = "secret.key"
                self.encryptor.save_key_to_file(filename)
                print(f"✅ Key saved to {filename}")
            else:
                print("No key to save!")
        
        elif choice == '4':
            filename = input("Enter filename to load (default: secret.key): ")
            if not filename:
                filename = "secret.key"
            if self.encryptor.load_key_from_file(filename):
                print(f"✅ Key loaded from {filename}")
            else:
                print(f"❌ File {filename} not found!")
        
        elif choice == '5':
            key_input = input("Enter key string: ")
            try:
                self.encryptor.load_key(key_input)
                print("✅ Key loaded successfully!")
            except Exception:
                print("❌ Invalid key format!")
    
    def file_operations_menu(self):
        """Handle file operations"""
        self.clear_screen()
        self.print_header()
        print("\n--- FILE OPERATIONS ---")
        
        files = self.file_handler.list_encrypted_files()
        
        if not files:
            print("\nNo encrypted files found in 'encrypted_files' directory.")
            return
        
        print("\nAvailable encrypted files:")
        for i, f in enumerate(files, 1):
            print(f"{i}. {f}")
        
        choice = input("\nSelect file number to view (or 0 to cancel): ")
        try:
            idx = int(choice) - 1
            if idx >= 0:
                filename = f"{self.file_handler.default_dir}/{files[idx]}"
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"\n--- Content of {files[idx]} ---")
                print(content[:500] + "..." if len(content) > 500 else content)
        except (ValueError, IndexError):
            pass
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_header()
            print(f"Current Method: {self.current_method.upper()}")
            self.print_menu()
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                self.encrypt_text_menu()
            elif choice == '2':
                self.decrypt_text_menu()
            elif choice == '3':
                self.switch_method_menu()
            elif choice == '4':
                self.key_management_menu()
            elif choice == '5':
                self.file_operations_menu()
            elif choice == '6':
                print("\nThank you for using Text Encryption Tool!")
                sys.exit(0)
            else:
                print("Invalid choice! Press Enter to continue...")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    app = TextEncryptionTool()
    app.run()
