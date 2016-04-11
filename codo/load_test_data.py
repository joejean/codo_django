import subprocess


args = ["python","manage.py","loadtestdata", "auth.User:2", "campaigns.Organizer:2", 
	"campaigns.Campaign:2", "campaigns.Reward:4", "challenges.AmountLog:2",
	"challenges.Log:2", "challenges.Identifier:2", "challenges.Membership:2",
	"challenges.Condition:2","challenges.ChallengeLink:2"  ]

subprocess.call(args)