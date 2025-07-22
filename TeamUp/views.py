from django.shortcuts import render, redirect
import random

def home(request):
    if request.method == 'POST':
        participants = request.POST.get('participants', '').split('\n')
        participants = [p.strip() for p in participants if p.strip()]
        num_teams = int(request.POST.get('num_teams', 2))
        activity_type = 'Team Activity'  # Default activity type since field was removed
        if participants and num_teams > 0:
            # Store participants and num_teams in session for reshuffling
            request.session['participants'] = participants
            request.session['num_teams'] = num_teams
            request.session['activity_type'] = activity_type
            
            random.shuffle(participants)
            teams = [[] for _ in range(num_teams)]
            for idx, participant in enumerate(participants):
                teams[idx % num_teams].append(participant)
            return render(request, 'teams.html', {
                'teams': teams, 
                'activity_type': activity_type,
                'total_participants': len(participants)
            })
    return render(request, 'home.html')

def reshuffle_teams(request):
    # Get stored data from session
    participants = request.session.get('participants', [])
    num_teams = request.session.get('num_teams', 2)
    activity_type = request.session.get('activity_type', 'Team Activity')
    
    if participants and num_teams > 0:
        # Shuffle participants again
        random.shuffle(participants)
        teams = [[] for _ in range(num_teams)]
        for idx, participant in enumerate(participants):
            teams[idx % num_teams].append(participant)
        return render(request, 'teams.html', {
            'teams': teams, 
            'activity_type': activity_type,
            'total_participants': len(participants)
        })
    else:
        # If no session data, redirect to home
        return redirect('home')
