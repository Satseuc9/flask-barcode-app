from flask import Flask, render_template, request
import barcode
from barcode.writer import ImageWriter
import io
import base64

app = Flask(__name__)

# List of valid stores
valid_stores = [293, 482, 3452, 3509, 3542, 3579, 4465, 4466, 4468, 4618, 5094, 5353, 7309, 7357, 7361]

def generate_barcode_image(data):
    """Generate barcode image and return base64 encoding"""
    barcode_class = barcode.get_barcode_class('code128')
    barcode_instance = barcode_class(data, writer=ImageWriter())
    
    # Save the barcode to a BytesIO object in memory
    buffer = io.BytesIO()
    barcode_instance.write(buffer)
    
    # Convert to base64
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str

@app.route("/", methods=["GET", "POST"])
def index():
    barcodes = []
    if request.method == "POST":
        store_number = request.form.get("store_number")
        carton_numbers = request.form.get("carton_numbers").splitlines()

        # Filter carton numbers that are valid (in this case, they should be 3 digits long)
        valid_carton_numbers = [num for num in carton_numbers if num.isdigit() and len(num) == 3]

        if store_number not in [str(store) for store in valid_stores]:
            error = "Invalid store number."
            return render_template("index.html", error=error)

        # Generate barcodes for the valid carton numbers
        for carton_number in valid_carton_numbers:
            # Combine store number and carton number to create the full barcode sequence
            full_barcode = store_number + carton_number  # Concatenate store number + carton number
            print(f"Generated Barcode: {full_barcode}")  # Debug line to see the full barcode sequence
            barcode_img = generate_barcode_image(full_barcode)
            barcodes.append((full_barcode, barcode_img))
    
    return render_template("index.html", barcodes=barcodes)

if __name__ == "__main__":
    app.run(debug=True)
