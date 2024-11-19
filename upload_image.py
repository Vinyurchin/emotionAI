import base64
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from process_image import process_image

class UploadHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        print("Handling OPTIONS request")
        self._set_headers()

    def do_POST(self):
        print("Handling POST request")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("Received POST data:", post_data)

        data = json.loads(post_data)
        print("Parsed JSON data:", data)
        
        image_data = data['image'].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        print("Decoded image data")

        image_path = "uploaded_image.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        print("Saved uploaded image to", image_path)
        
        # Check if the image was saved successfully
        if os.path.exists(image_path):
            processed_image_path = process_image(image_path)
            if processed_image_path:
                response_message = f"Image uploaded and processed successfully. Processed image saved at: {processed_image_path}"
                print("Processed image path:", processed_image_path)
            else:
                response_message = "Failed to process the image."
                print("Failed to process the image")
        else:
            response_message = "Failed to save the uploaded image."
            print("Failed to save the uploaded image")
        
        self._set_headers()
        self.wfile.write(response_message.encode())
        print("Response sent")

def run(server_class=HTTPServer, handler_class=UploadHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()