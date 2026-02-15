import cv2
import time
import layered_rock
import red_oxide
import glass_oxide

def main():
    # Process images from marslr0 to marslr3
    for i in range(5):
        filename = f"/home/atharv/Documents/Antigravity Projects/RandomStuff/ISRO/images/marslr{i}.png"
        print(f"\nProcessing {filename}...")
        
        # Load the image
        frame = cv2.imread(filename)

        if frame is None:
            print(f"Error: Could not read image {filename}. Skipping.")
            continue
        
        # Process the image with the three modules
        prob_layered = layered_rock.process_image(frame)
        prob_red = red_oxide.process_image(frame)
        prob_glass = glass_oxide.process_image(frame)
        
        # Create the probability vector
        probability_vector = [prob_layered, prob_red, prob_glass]
        
        # Output the results
        print("-" * 30)
        print("Processing Results:")
        print(f"Layered Rock Probability: {prob_layered:.4f}")
        print(f"Red Oxide Probability:    {prob_red:.4f}")
        print(f"Glass Oxide Probability:  {prob_glass:.4f}")
        print("-" * 30)
        print(f"Final Probability Vector: {probability_vector}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
