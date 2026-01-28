"""
Eye Tracker Module

Handles eye gaze estimation using MediaPipe Face Mesh.
Tracks iris position and estimates gaze direction for screen mapping.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, List


class EyeTracker:
    """
    Eye gaze estimation using MediaPipe Face Mesh with iris landmarks.
    
    Uses 468 face landmarks + 10 iris landmarks (5 per eye) to:
    - Detect face and eye regions
    - Track iris center position
    - Estimate gaze direction
    - Map gaze to screen coordinates
    """
    
    # Face Mesh landmark indices for eyes
    # Left eye landmarks
    LEFT_EYE_OUTER = 33
    LEFT_EYE_INNER = 133
    LEFT_EYE_TOP = 159
    LEFT_EYE_BOTTOM = 145
    LEFT_IRIS_CENTER = 468  # Iris landmarks start at 468
    
    # Right eye landmarks
    RIGHT_EYE_OUTER = 362
    RIGHT_EYE_INNER = 263
    RIGHT_EYE_TOP = 386
    RIGHT_EYE_BOTTOM = 374
    RIGHT_IRIS_CENTER = 473  # Right iris center
    
    # Eye corners for aspect ratio
    LEFT_EYE_POINTS = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_POINTS = [362, 385, 387, 263, 373, 380]
    
    def __init__(
        self,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7
    ):
        """
        Initialize eye tracker.
        
        Args:
            detection_confidence: Minimum face detection confidence
            tracking_confidence: Minimum face tracking confidence
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_styles = mp.solutions.drawing_styles
        
        # Initialize Face Mesh with iris refinement
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,  # Enables iris landmarks
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        
        self.landmarks = None
        self.face_detected = False
        
        # Gaze tracking
        self.gaze_point: Optional[Tuple[int, int]] = None
        self.left_iris_center: Optional[Tuple[int, int]] = None
        self.right_iris_center: Optional[Tuple[int, int]] = None
        
        # Calibration data (normalized gaze ratios)
        self.calibrated = False
        self.calibration_points: List[Tuple[float, float]] = []
        
        # Smoothing
        self.prev_gaze_x: Optional[float] = None
        self.prev_gaze_y: Optional[float] = None
        self.smoothing = 0.6
        
        # Blink detection
        self.blink_threshold = 0.2
        self.is_blinking = False
        
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a video frame for eye gaze estimation.
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            Processed frame with eye landmarks drawn
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        self.face_detected = False
        self.landmarks = None
        self.left_iris_center = None
        self.right_iris_center = None
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.face_detected = True
                self.landmarks = face_landmarks
                
                h, w = frame.shape[:2]
                
                # Get iris centers
                self.left_iris_center = self._get_landmark_position(
                    self.LEFT_IRIS_CENTER, w, h
                )
                self.right_iris_center = self._get_landmark_position(
                    self.RIGHT_IRIS_CENTER, w, h
                )
                
                # Draw eye contours
                self._draw_eye_landmarks(frame, w, h)
                
                # Calculate gaze
                self._calculate_gaze(w, h)
                
        return frame
    
    def _get_landmark_position(
        self, 
        landmark_id: int, 
        frame_width: int, 
        frame_height: int
    ) -> Optional[Tuple[int, int]]:
        """Get pixel position of a specific landmark."""
        if not self.landmarks or landmark_id >= len(self.landmarks.landmark):
            return None
            
        landmark = self.landmarks.landmark[landmark_id]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        
        return (x, y)
    
    def _draw_eye_landmarks(self, frame: np.ndarray, w: int, h: int):
        """Draw eye contours and iris centers on frame."""
        if not self.landmarks:
            return
            
        # Draw left eye contour
        left_eye_pts = []
        for idx in self.LEFT_EYE_POINTS:
            pt = self._get_landmark_position(idx, w, h)
            if pt:
                left_eye_pts.append(pt)
        if len(left_eye_pts) >= 4:
            pts = np.array(left_eye_pts, dtype=np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 255), 1)
        
        # Draw right eye contour
        right_eye_pts = []
        for idx in self.RIGHT_EYE_POINTS:
            pt = self._get_landmark_position(idx, w, h)
            if pt:
                right_eye_pts.append(pt)
        if len(right_eye_pts) >= 4:
            pts = np.array(right_eye_pts, dtype=np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 255), 1)
        
        # Draw iris centers
        if self.left_iris_center:
            cv2.circle(frame, self.left_iris_center, 3, (0, 255, 0), -1)
        if self.right_iris_center:
            cv2.circle(frame, self.right_iris_center, 3, (0, 255, 0), -1)
    
    def _calculate_gaze(self, frame_width: int, frame_height: int):
        """Calculate gaze direction from iris positions."""
        if not self.landmarks:
            return
            
        # Get eye corner positions for reference
        left_outer = self._get_landmark_position(self.LEFT_EYE_OUTER, frame_width, frame_height)
        left_inner = self._get_landmark_position(self.LEFT_EYE_INNER, frame_width, frame_height)
        right_outer = self._get_landmark_position(self.RIGHT_EYE_OUTER, frame_width, frame_height)
        right_inner = self._get_landmark_position(self.RIGHT_EYE_INNER, frame_width, frame_height)
        
        if not all([left_outer, left_inner, right_outer, right_inner,
                   self.left_iris_center, self.right_iris_center]):
            return
        
        # Calculate iris position ratio within eye (0 = outer, 1 = inner)
        left_eye_width = abs(left_inner[0] - left_outer[0])
        right_eye_width = abs(right_inner[0] - right_outer[0])
        
        if left_eye_width < 5 or right_eye_width < 5:
            return
        
        # Normalize iris position within eye
        left_ratio_x = (self.left_iris_center[0] - left_outer[0]) / left_eye_width
        right_ratio_x = (self.right_iris_center[0] - right_outer[0]) / right_eye_width
        
        # Average both eyes
        avg_ratio_x = (left_ratio_x + right_ratio_x) / 2
        
        # For vertical, use eye top/bottom
        left_top = self._get_landmark_position(self.LEFT_EYE_TOP, frame_width, frame_height)
        left_bottom = self._get_landmark_position(self.LEFT_EYE_BOTTOM, frame_width, frame_height)
        right_top = self._get_landmark_position(self.RIGHT_EYE_TOP, frame_width, frame_height)
        right_bottom = self._get_landmark_position(self.RIGHT_EYE_BOTTOM, frame_width, frame_height)
        
        if all([left_top, left_bottom, right_top, right_bottom]):
            left_eye_height = abs(left_bottom[1] - left_top[1])
            right_eye_height = abs(right_bottom[1] - right_top[1])
            
            if left_eye_height > 3 and right_eye_height > 3:
                left_ratio_y = (self.left_iris_center[1] - left_top[1]) / left_eye_height
                right_ratio_y = (self.right_iris_center[1] - right_top[1]) / right_eye_height
                avg_ratio_y = (left_ratio_y + right_ratio_y) / 2
            else:
                avg_ratio_y = 0.5
        else:
            avg_ratio_y = 0.5
        
        # Store gaze ratios (will be mapped to screen in get_gaze_point)
        self._gaze_ratio_x = avg_ratio_x
        self._gaze_ratio_y = avg_ratio_y
    
    def get_gaze_point(
        self, 
        screen_width: int, 
        screen_height: int
    ) -> Optional[Tuple[int, int]]:
        """
        Get estimated screen gaze point.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            
        Returns:
            Tuple of (x, y) screen coordinates or None
        """
        if not self.face_detected or not hasattr(self, '_gaze_ratio_x'):
            return None
        
        # Map gaze ratio to screen coordinates
        # Gaze ratio typically ranges from ~0.3 to ~0.7 for normal eye movement
        # Expand this range to full screen
        
        # Normalize to 0-1 range (expand from typical 0.3-0.7 range)
        norm_x = (self._gaze_ratio_x - 0.3) / 0.4
        norm_y = (self._gaze_ratio_y - 0.3) / 0.4
        
        # Clamp to 0-1
        norm_x = max(0, min(1, norm_x))
        norm_y = max(0, min(1, norm_y))
        
        # Invert X for natural movement (look right = cursor right)
        norm_x = 1 - norm_x
        
        # Map to screen
        screen_x = int(norm_x * screen_width)
        screen_y = int(norm_y * screen_height)
        
        # Apply smoothing
        if self.prev_gaze_x is not None and self.prev_gaze_y is not None:
            screen_x = int(self.prev_gaze_x + (screen_x - self.prev_gaze_x) * (1 - self.smoothing))
            screen_y = int(self.prev_gaze_y + (screen_y - self.prev_gaze_y) * (1 - self.smoothing))
        
        self.prev_gaze_x = screen_x
        self.prev_gaze_y = screen_y
        
        # Clamp to screen bounds
        screen_x = max(0, min(screen_x, screen_width - 1))
        screen_y = max(0, min(screen_y, screen_height - 1))
        
        return (screen_x, screen_y)
    
    def get_eye_aspect_ratio(self) -> float:
        """
        Calculate Eye Aspect Ratio (EAR) for blink detection.
        
        Returns:
            EAR value (lower = more closed)
        """
        if not self.landmarks:
            return 1.0
        
        # Simplified EAR using top/bottom landmarks
        # EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
        # For our purposes, we'll use a simplified version
        
        left_top = self._get_landmark_position(self.LEFT_EYE_TOP, 100, 100)
        left_bottom = self._get_landmark_position(self.LEFT_EYE_BOTTOM, 100, 100)
        left_outer = self._get_landmark_position(self.LEFT_EYE_OUTER, 100, 100)
        left_inner = self._get_landmark_position(self.LEFT_EYE_INNER, 100, 100)
        
        if not all([left_top, left_bottom, left_outer, left_inner]):
            return 1.0
        
        vertical = abs(left_bottom[1] - left_top[1])
        horizontal = abs(left_inner[0] - left_outer[0])
        
        if horizontal == 0:
            return 1.0
            
        ear = vertical / horizontal
        return ear
    
    def is_blink_detected(self) -> bool:
        """Check if eyes are blinking/closed."""
        ear = self.get_eye_aspect_ratio()
        self.is_blinking = ear < self.blink_threshold
        return self.is_blinking
    
    def set_smoothing(self, smoothing: float):
        """Update gaze smoothing factor."""
        self.smoothing = max(0, min(1, smoothing))
    
    def reset(self):
        """Reset tracking state."""
        self.prev_gaze_x = None
        self.prev_gaze_y = None
        
    def release(self):
        """Release resources."""
        if self.face_mesh:
            self.face_mesh.close()
