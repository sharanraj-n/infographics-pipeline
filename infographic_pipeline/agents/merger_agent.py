"""
Agent for merging content and infographic layout into a unified design.
Straightforward: just packs them together in a dict.
"""

class MergerAgent:
    def merge(self, content_data, design_spec):
        """
        Combines structured content and design spec under a 'merged_layout' key.
        """
        return {
            "merged_layout": {
                "content_blocks": content_data,
                "design_guide": design_spec,
                "layout_style": "balanced composition"
            }
        }
