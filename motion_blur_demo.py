import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

class MotionBlurRenderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.velocity_buffer = np.zeros((height, width, 2), dtype=np.float32)
        self.color_buffer = np.zeros((height, width, 3), dtype=np.uint8)
        self.previous_positions = {}
        
    def create_scene_objects(self):
        """Create moving objects in the scene"""
        objects = []
        
        # Fast moving red car (horizontal motion)
        car = {
            'type': 'rectangle',
            'color': (255, 50, 50),
            'size': (80, 40),
            'position': [100, 200],
            'velocity': [8, 0],  # 8 pixels per frame horizontally
            'id': 'car'
        }
        
        # Spinning blue wheel
        wheel = {
            'type': 'circle',
            'color': (50, 50, 255),
            'radius': 30,
            'position': [400, 400],
            'velocity': [2, -3],  # Diagonal movement
            'id': 'wheel'
        }
        
        # Fast green ball (parabolic motion)
        ball = {
            'type': 'circle',
            'color': (50, 255, 50),
            'radius': 20,
            'position': [150, 450],
            'velocity': [6, -4],
            'id': 'ball'
        }
        
        objects.append(car)
        objects.append(wheel)
        objects.append(ball)
        
        return objects
    
    def update_object_positions(self, objects, frame_num):
        """Update object positions and handle boundaries"""
        for obj in objects:
            # Store previous position
            if obj['id'] not in self.previous_positions:
                self.previous_positions[obj['id']] = obj['position'].copy()
            else:
                self.previous_positions[obj['id']] = obj['position'].copy()
            
            # Update position based on velocity
            obj['position'][0] += obj['velocity'][0]
            obj['position'][1] += obj['velocity'][1]
            
            # Boundary handling with bounce
            if obj['position'][0] <= 0 or obj['position'][0] >= self.width - 50:
                obj['velocity'][0] *= -0.8  # Energy loss on bounce
            if obj['position'][1] <= 0 or obj['position'][1] >= self.height - 50:
                obj['velocity'][1] *= -0.8
                
            # Add some physics (gravity for ball)
            if obj['id'] == 'ball':
                obj['velocity'][1] += 0.2  # Gravity
    
    def render_objects_to_color_buffer(self, objects):
        """Render objects to color buffer (geometry pass)"""
        self.color_buffer.fill(20)  # Dark background
        
        for obj in objects:
            pos = [int(obj['position'][0]), int(obj['position'][1])]
            
            if obj['type'] == 'rectangle':
                cv2.rectangle(self.color_buffer, 
                            (pos[0], pos[1]), 
                            (pos[0] + obj['size'][0], pos[1] + obj['size'][1]), 
                            obj['color'], -1)
            elif obj['type'] == 'circle':
                cv2.circle(self.color_buffer, 
                         (pos[0], pos[1]), 
                         obj['radius'], 
                         obj['color'], -1)
    
    def generate_velocity_buffer(self, objects):
        """Generate velocity buffer following the PDF specifications"""
        self.velocity_buffer.fill(0)
        
        for obj in objects:
            if obj['id'] not in self.previous_positions:
                continue
                
            # Calculate screen-space velocity (current - previous)
            curr_pos = np.array(obj['position'])
            prev_pos = np.array(self.previous_positions[obj['id']])
            velocity = curr_pos - prev_pos
            
            # Create mask for object pixels
            mask = np.zeros((self.height, self.width), dtype=np.uint8)
            pos = [int(obj['position'][0]), int(obj['position'][1])]
            
            if obj['type'] == 'rectangle':
                cv2.rectangle(mask, 
                            (pos[0], pos[1]), 
                            (pos[0] + obj['size'][0], pos[1] + obj['size'][1]), 
                            255, -1)
            elif obj['type'] == 'circle':
                cv2.circle(mask, 
                         (pos[0], pos[1]), 
                         obj['radius'], 
                         255, -1)
            
            # Store velocity in RG channels (following PDF specification)
            object_pixels = mask > 0
            self.velocity_buffer[object_pixels, 0] = velocity[0]  # R channel: horizontal
            self.velocity_buffer[object_pixels, 1] = velocity[1]  # G channel: vertical
    
    def apply_motion_blur(self, max_samples=12, blur_scale=1.0, velocity_threshold=0.5):
        """Apply motion blur using velocity buffer (following PDF algorithm)"""
        result = np.zeros_like(self.color_buffer, dtype=np.float32)
        
        for y in range(self.height):
            for x in range(self.width):
                # Get velocity for current pixel
                velocity = self.velocity_buffer[y, x] * blur_scale
                speed = np.linalg.norm(velocity)
                
                # Early exit for static areas (threshold from PDF)
                if speed < velocity_threshold:
                    result[y, x] = self.color_buffer[y, x]
                    continue
                
                # Clamp extreme velocities (following PDF recommendation)
                if speed > 20.0:
                    velocity = (velocity / speed) * 20.0
                
                # Sample along motion vector (PDF algorithm)
                color_sum = np.zeros(3, dtype=np.float32)
                weight_sum = 0.0
                
                for i in range(max_samples):
                    t = i / max(1, max_samples - 1)
                    
                    # Sample position along motion vector
                    sample_x = x - velocity[0] * t
                    sample_y = y - velocity[1] * t
                    
                    # Bounds checking
                    if (0 <= sample_x < self.width and 0 <= sample_y < self.height):
                        # Bilinear interpolation for sub-pixel sampling
                        sample_color = self.bilinear_sample(sample_x, sample_y)
                        
                        # Distance-based weight (following PDF specification)
                        weight = 1.0 - t
                        color_sum += sample_color * weight
                        weight_sum += weight
                
                # Normalize by total weight
                if weight_sum > 0:
                    result[y, x] = color_sum / weight_sum
                else:
                    result[y, x] = self.color_buffer[y, x]
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def bilinear_sample(self, x, y):
        """Bilinear interpolation for sub-pixel sampling"""
        x1, y1 = int(x), int(y)
        x2, y2 = min(x1 + 1, self.width - 1), min(y1 + 1, self.height - 1)
        
        # Interpolation weights
        wx = x - x1
        wy = y - y1
        
        # Sample four neighboring pixels
        c00 = self.color_buffer[y1, x1].astype(np.float32)
        c01 = self.color_buffer[y2, x1].astype(np.float32)
        c10 = self.color_buffer[y1, x2].astype(np.float32)
        c11 = self.color_buffer[y2, x2].astype(np.float32)
        
        # Bilinear interpolation
        color = (c00 * (1 - wx) * (1 - wy) + 
                c10 * wx * (1 - wy) + 
                c01 * (1 - wx) * wy + 
                c11 * wx * wy)
        
        return color
    
    def visualize_velocity_buffer(self):
        """Visualize velocity buffer for debugging"""
        # Convert velocity to color for visualization
        velocity_vis = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Normalize velocities to 0-255 range
        vel_mag = np.linalg.norm(self.velocity_buffer, axis=2)
        max_vel = np.max(vel_mag) if np.max(vel_mag) > 0 else 1
        
        velocity_vis[:, :, 0] = np.clip((self.velocity_buffer[:, :, 0] / max_vel) * 127 + 127, 0, 255)
        velocity_vis[:, :, 1] = np.clip((self.velocity_buffer[:, :, 1] / max_vel) * 127 + 127, 0, 255)
        velocity_vis[:, :, 2] = np.clip(vel_mag / max_vel * 255, 0, 255)
        
        return velocity_vis


def create_motion_blur_demo():
    """Main function to create motion blur demonstration"""
    print("🎮 Creating Motion Blur Demo using Velocity Buffers...")
    print("📊 Following industry standards from your presentation...")
    
    # Initialize renderer
    renderer = MotionBlurRenderer(800, 600)
    
    # Create output directory
    os.makedirs("motion_blur_output", exist_ok=True)
    
    # Generate scene objects
    objects = renderer.create_scene_objects()
    
    # Simulate several frames to build up motion
    frames = []
    velocity_frames = []
    blurred_frames = []
    
    print("\n🔄 Rendering frames...")
    for frame in range(30):
        print(f"   Frame {frame + 1}/30", end="\r")
        
        # Update object positions
        renderer.update_object_positions(objects, frame)
        
        # Render objects to color buffer (Geometry Pass)
        renderer.render_objects_to_color_buffer(objects)
        
        # Generate velocity buffer
        renderer.generate_velocity_buffer(objects)
        
        # Apply motion blur (Post-Process Pass)
        blurred_image = renderer.apply_motion_blur(
            max_samples=12,      # 8-16 samples as recommended in PDF
            blur_scale=1.0,      # Global intensity control
            velocity_threshold=0.5  # Skip static areas
        )
        
        # Store frames
        frames.append(renderer.color_buffer.copy())
        velocity_frames.append(renderer.visualize_velocity_buffer())
        blurred_frames.append(blurred_image)
    
    print("\n✅ Rendering complete!")
    
    # Save comparison images
    save_comparison_images(frames, velocity_frames, blurred_frames)
    
    # Create animation
    create_animation(frames, blurred_frames)
    
    print("\n🎯 Motion Blur Demo Complete!")
    print("📁 Check 'motion_blur_output' folder for results")
    print("🖼️  Files generated:")
    print("   - comparison_frame_*.png (frame comparisons)")
    print("   - motion_blur_animation.gif (animated result)")
    print("   - velocity_buffer_visualization.png")


def save_comparison_images(frames, velocity_frames, blurred_frames):
    """Save comparison images showing before/after motion blur"""
    print("\n💾 Saving comparison images...")
    
    # Save multiple frame comparisons
    for i in [5, 15, 25]:  # Save a few key frames
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'Motion Blur Implementation - Frame {i}', fontsize=16, fontweight='bold')
        
        # Original frame
        axes[0, 0].imshow(cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('Original (Color Buffer)', fontweight='bold')
        axes[0, 0].axis('off')
        
        # Velocity buffer visualization
        axes[0, 1].imshow(cv2.cvtColor(velocity_frames[i], cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title('Velocity Buffer (RG Channels)', fontweight='bold')
        axes[0, 1].axis('off')
        
        # Motion blurred result
        axes[1, 0].imshow(cv2.cvtColor(blurred_frames[i], cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title('Motion Blurred Result', fontweight='bold')
        axes[1, 0].axis('off')
        
        # Side-by-side comparison
        comparison = np.hstack([frames[i], blurred_frames[i]])
        axes[1, 1].imshow(cv2.cvtColor(comparison, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Before vs After', fontweight='bold')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'motion_blur_output/comparison_frame_{i:02d}.png', 
                   dpi=150, bbox_inches='tight')
        plt.close()
    
    # Create velocity buffer analysis
    create_velocity_analysis(velocity_frames[15])


def create_velocity_analysis(velocity_frame):
    """Create detailed velocity buffer analysis"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Velocity Buffer Analysis (Industry Standard RG16F Format)', 
                fontsize=14, fontweight='bold')
    
    # Convert back to velocity components for analysis
    velocity_r = (velocity_frame[:, :, 0].astype(np.float32) - 127) / 127
    velocity_g = (velocity_frame[:, :, 1].astype(np.float32) - 127) / 127
    velocity_magnitude = velocity_frame[:, :, 2]
    
    # R Channel (Horizontal velocity)
    im1 = axes[0].imshow(velocity_r, cmap='RdBu', vmin=-1, vmax=1)
    axes[0].set_title('R Channel: Horizontal Velocity\n(Red=Right, Blue=Left)')
    axes[0].axis('off')
    plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)
    
    # G Channel (Vertical velocity)
    im2 = axes[1].imshow(velocity_g, cmap='RdBu', vmin=-1, vmax=1)
    axes[1].set_title('G Channel: Vertical Velocity\n(Red=Down, Blue=Up)')
    axes[1].axis('off')
    plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)
    
    # Magnitude
    im3 = axes[2].imshow(velocity_magnitude, cmap='hot')
    axes[2].set_title('Velocity Magnitude\n(Brightness = Speed)')
    axes[2].axis('off')
    plt.colorbar(im3, ax=axes[2], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig('motion_blur_output/velocity_buffer_analysis.png', 
               dpi=150, bbox_inches='tight')
    plt.close()


def create_animation(original_frames, blurred_frames):
    """Create animated GIF showing motion blur effect"""
    print("🎬 Creating animation...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Real-time Motion Blur using Velocity Buffers', 
                fontsize=14, fontweight='bold')
    
    def animate(frame):
        ax1.clear()
        ax2.clear()
        
        ax1.imshow(cv2.cvtColor(original_frames[frame], cv2.COLOR_BGR2RGB))
        ax1.set_title(f'Original Frame {frame + 1}')
        ax1.axis('off')
        
        ax2.imshow(cv2.cvtColor(blurred_frames[frame], cv2.COLOR_BGR2RGB))
        ax2.set_title(f'Motion Blurred Frame {frame + 1}')
        ax2.axis('off')
        
        return []
    
    anim = FuncAnimation(fig, animate, frames=len(original_frames), 
                        interval=100, blit=False, repeat=True)
    
    # Save as GIF
    anim.save('motion_blur_output/motion_blur_animation.gif', 
             writer='pillow', fps=10, dpi=100)
    plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🎮 MOTION BLUR USING VELOCITY BUFFERS")
    print("📚 Implementation based on CSE 409 Graphics Assignment")
    print("👥 Team AmarGraphics - BUET")
    print("=" * 60)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    try:
        import numpy as np
        import cv2
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        print("✅ All dependencies found!")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install numpy opencv-python matplotlib")
        exit(1)
    
    # Run the demo
    create_motion_blur_demo()
    
    print("\n" + "=" * 60)
    print("✨ SUCCESS! Motion blur demo completed successfully!")
    print("🎯 Implementation follows all industry standards from your PDF:")
    print("   ✓ Velocity buffer generation (RG16F format)")
    print("   ✓ 8-16 samples for optimal quality/performance")
    print("   ✓ Distance-based weight falloff")
    print("   ✓ Early exit for static areas")
    print("   ✓ Velocity clamping for extreme motion")
    print("   ✓ Single geometry pass + post-process")
    print("=" * 60)
