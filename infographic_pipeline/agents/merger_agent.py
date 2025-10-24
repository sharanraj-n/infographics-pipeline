class MergerAgent:
    def merge(self, content_data, design_spec):
        """
        Combine extracted content and design spec into one output dict.
        """
        return {
            "merged_layout": {
                "content_blocks": content_data,
                "design_guide": design_spec,
                "layout_style": "balanced composition"
            }
        }
