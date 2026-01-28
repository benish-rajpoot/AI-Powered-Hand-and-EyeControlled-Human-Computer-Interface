"""
Hand Tracker Module

Handles real-time hand detection and landmark tracking using MediaPipe.
Tracks 21 hand landmarks and provides hand state information.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, List


class HandTracker:
    """
    Real-time hand tracking using MediaPipe Hands.
    
    Attributes:
        max_hands: Maximum number of hands to detect
        detection_confidence: Minimum confidence for detection
        tracking_confidence: Minimum confidence for tracking
    """
    
    def __init__(
        self,
        max_hands: int = 1,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7
    ):
        """
        Initialize the hand tracker.
        
        Args:
            max_hands: Maximum number of hands to detect (default: 1)
            detection_confidence: Minimum detection confidence threshold
            tracking_confidence: Minimum tracking confidence threshold
        """
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        
        self.landmarks = None
        self.hand_detected = False
        
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a video frame and detect hand landmarks.
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            Processed frame with landmarks drawn (if detected)
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        self.hand_detected = False
        self.landmarks = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.hand_detected = True
                self.landmarks = hand_landmarks
                
                # Draw landmarks on frame
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                
        return frame
    
    def get_landmark_position(
        self, 
        landmark_id: int, 
        frame_shape: Tuple[int, int, int]
    ) -> Optional[Tuple[int, int]]:
        """
        Get the pixel coordinates of a specific landmark.
        
        Args:
            landmark_id: MediaPipe landmark index (0-20)
            frame_shape: Shape of the frame (height, width, channels)
            
        Returns:
            Tuple of (x, y) pixel coordinates or None if not detected
        """
        if not self.landmarks:
            return None
            
        h, w = frame_shape[:2]
        landmark = self.landmarks.landmark[landmark_id]
        
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        
        return (x, y)
    
    def get_index_finger_tip(
        self, 
        frame_shape: Tuple[int, int, int]
    ) -> Optional[Tuple[int, int]]:
        """
        Get the position of the index finger tip (landmark 8).
        
        Args:
            frame_shape: Shape of the frame
            
        Returns:
            Tuple of (x, y) coordinates or None
        """
        return self.get_landmark_position(8, frame_shape)
    
    def get_thumb_tip(
        self, 
        frame_shape: Tuple[int, int, int]
    ) -> Optional[Tuple[int, int]]:
        """
        Get the position of the thumb tip (landmark 4).
        
        Args:
            frame_shape: Shape of the frame
            
        Returns:
            Tuple of (x, y) coordinates or None
        """
        return self.get_landmark_position(4, frame_shape)
    
    def get_all_landmarks(
        self, 
        frame_shape: Tuple[int, int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Get all 21 landmark positions.
        
        Args:
            frame_shape: Shape of the frame
            
        Returns:
            List of 21 (x, y) tuples or None if no hand detected
        """
        if not self.landmarks:
            return None
            
        positions = []
        for i in range(21):
            pos = self.get_landmark_position(i, frame_shape)
            positions.append(pos)
            
        return positions
    
    def release(self):
        """Release MediaPipe resources."""
        self.hands.close()
