#!usr/bin/env python

class Goals():
	def __init__(self):
		import glob
		import json
		self.global_goals = []
		for goal in glob.glob("goals/global/*"):
			with open(goal, "r") as f:
				data = json.load(f)
				self.global_goals.append(data)
		print self.goals

	def addGoal(self):
		goal = raw_input("Goal: ")
		importance = input("Importance (1-10): ")
		parents = raw_input("Parents: ") # multiple parents?
		subgoals = raw_input("Subgoals: ") # have to parse subgoals
		goal_json={"goal":goal,
			"importance":importance,
			"parents":parents,
			"subgoals":subgoals}
		import json
		with open("goals/"+goal+".json", 'w') as f:
   			 json.dump(goal_json, f)
		
		

