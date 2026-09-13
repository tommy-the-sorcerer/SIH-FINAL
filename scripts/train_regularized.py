from ultralytics import YOLO

if __name__ == '__main__':
    # Load base model
    model = YOLO("yolov8m.pt")

    # Start training with anti-overfitting pipeline
    results = model.train(
        data="/content/dataset/data.yaml",  # Update path if running locally
        epochs=100,  # Max limit (Early Stopping will stop earlier)

        # --- 1. EARLY STOPPING ---
        patience=10,  # Stop if validation mAP does not improve for 10 epochs

        # --- 2. REGULARIZATION TECHNIQUES ---
        weight_decay=0.001,  # L2 Regularization penalty
        dropout=0.2,  # 20% Dropout in classification layers
        label_smoothing=0.1,  # Softens target labels to prevent overconfidence

        # --- 3. ANTI-OVERFITTING AUGMENTATIONS ---
        mosaic=1.0,  # Combines 4 images into 1 grid
        mixup=0.15,  # Blends image pairs to soften decision boundaries
        erasing=0.4,  # Randomly hides image patches to force feature spread
        degrees=15.0,  # Random rotation (+/- 15 deg)
        translate=0.1,  # Random position translation
        scale=0.5,  # Random zoom in/out
        hsv_h=0.015,  # Color hue variation
        hsv_s=0.7,  # Saturation variation
        hsv_v=0.4,  # Brightness variation

        imgsz=640,
        batch=16,
        device=0,  # Use GPU
        workers=4,
        name="plantdoc_regularized"
    )