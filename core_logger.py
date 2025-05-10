import os
import json
import datetime

def current_timestamp():
	return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

class Logger:
	def __init__(self, base_dir="exp"):
		self.base_dir = base_dir
		self.experiment_dir = None
		self.manifest = {
			"render_id": "",
			"time": "",
			"manifest_version": "0.1",
			"origin": "",
			"plots": [],
			"plot_groups": {},
			"graph_path": "/",
			"render_templates": {},
			"style": {
				"default_colormap": "viridis",
				"theme": "dark"
			},
			"render_kit_version": "0.1.0"
		}

	def start_experiment(self, experiment_id, origin="default"):
		timestamp = current_timestamp()
		self.experiment_dir = os.path.join(self.base_dir, f"{experiment_id}_{timestamp}")
		os.makedirs(os.path.join(self.experiment_dir, "Singles"), exist_ok=True)

		self.manifest["render_id"] = experiment_id
		self.manifest["time"] = timestamp
		self.manifest["origin"] = origin

	def create_plot(self, name, data, meta=None, group=None, group_meta=None, template=None):
		if meta is None:
			meta = {}
		if template is None:
			template = meta.get("template", "matrix")

		# Save plot data under appropriate directory
		filename = f"{name}.plot.json"
		if group:
			group_dir = os.path.join(self.experiment_dir, group)
			os.makedirs(group_dir, exist_ok=True)
			file_path = os.path.join(group_dir, filename)
			source_path = f"{group}/{filename}"
		else:
			singles_dir = os.path.join(self.experiment_dir, "Singles")
			os.makedirs(singles_dir, exist_ok=True)
			file_path = os.path.join(singles_dir, filename)
			source_path = f"Singles/{filename}"

		plot_data = {
			"meta": {
				"name": name,
				"type": meta.get("type", "Unknown"),
				"template": template
			},
			"data": data
		}
		with open(file_path, "w") as f:
			json.dump(plot_data, f, indent=2)

		# Build the full plot entry
		plot_entry = {
			"name": name,
			"type": meta.get("type", "Unknown"),
			"source": source_path,
			"output": f"{name}.png"  # filename only!
		}

		# Track render templates
		if template not in self.manifest["render_templates"]:
			self.manifest["render_templates"][template] = {
				"template_path": template
			}

		# Handle plot groups and manifest registration
		if group:
			if group not in self.manifest["plot_groups"]:
				self.manifest["plot_groups"][group] = {
					"plots": [],
					"meta": group_meta or {}
				}
			self.manifest["plot_groups"][group]["plots"].append(plot_entry)
		else:
			self.manifest["plots"].append(plot_entry)

	def set_style(self, colormap="viridis", theme="dark"):
		self.manifest["style"]["default_colormap"] = colormap
		self.manifest["style"]["theme"] = theme

	def finalize(self):
		# Save the manifest
		manifest_path = os.path.join(self.experiment_dir, "manifest.json")
		with open(manifest_path, "w") as f:
			json.dump(self.manifest, f, indent=2)

		print(f"[Logger] Experiment finalized: {manifest_path}")
