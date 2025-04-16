from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Leaderboard
import google.generativeai as genai
import re

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')




def start(request):
    if request.method == 'POST':
        num = int(request.POST['num'])
        category = request.POST['category']
        difficulty = request.POST['difficulty']
        qtype = request.POST['type']

        questions = generate_quiz_with_gemini(num, category, difficulty, qtype)
        request.session['quiz_data'] = questions
        return redirect('class_quiz')

    # GET method — extract category from query params and pass it to the template
    category_from_blog = request.GET.get('category', '')

    return render(request, 'cast.html', {'category': category_from_blog})

def startquiz(request):
    quiz_data = request.session.get('quiz_data', [])
    if 'user_answers' in request.session:
        del request.session['user_answers']
    return render(request, 'class.html', {
        'quiz_data': json.dumps(quiz_data)  # Serialize for JavaScript
    })# Now correctly populated
    return render(request, 'class.html', {'quiz_data': quiz_data})

genai.configure(api_key='AIzaSyDY0Gu2NWWORP1peDYzoLQPfUiL7eQMlfs')
def generate_quiz_with_gemini(num, category, difficulty, qtype):
    prompt = f"""
    Generate {num} {difficulty} level quiz questions in the category '{category}' with {qtype} type.
    Format each question like:
    {{
      "text": "Question?",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }}
    Return the output as a valid JSON list.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    # Remove markdown formatting if present
    if raw_text.startswith("```json"):
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
    elif raw_text.startswith("```"):
        raw_text = raw_text.replace("```", "").strip()

    # Extract the JSON list using regex
    match = re.search(r'\[\s*{.*}\s*\]', raw_text, re.DOTALL)
    if match:
        raw_text = match.group()

    # Attempt to parse JSON
    try:
        return json.loads(raw_text)
    except Exception as e:
        print(f"[Gemini Error] Failed to parse JSON: {e}")
        print("Raw response:", raw_text)
        return []
    
@csrf_exempt
def generate_quiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        num = data.get('numQuestions')
        category = data.get('category')
        difficulty = data.get('difficulty')
        qtype = data.get('type')
        
        questions = generate_quiz_with_gemini(num, category, difficulty, qtype)
        request.session['quiz_data'] = questions  # Add this line
        request.session.modified = True  # Ensure session is saved
        return JsonResponse({'questions': questions})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def result_view(request):
    if request.method == "POST":
        try:
            submitted_answers = json.loads(request.body)
            questions = request.session.get('quiz_data', [])
            
            if not questions:
                return JsonResponse({'error': 'No quiz data found'}, status=400)

            score = sum(
                1 for i, ans in enumerate(submitted_answers) 
                if i < len(questions) and ans == questions[i]['answer']
            )
            total = len(questions)
            percentage = round((score/total)*100, 2) if total > 0 else 0

            # Save to leaderboard only if authenticated
            if request.user.is_authenticated:
                Leaderboard.objects.create(
                    user=request.user,
                    username=request.user.username,
                    score=score,
                    total=total
                )

            return JsonResponse({
                'score': score,
                'total': total,
                'percentage': percentage
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    
def result_page_view(request):
    score = request.GET.get('score', 0)
    total = request.GET.get('total', 0)
    leaderboard = Leaderboard.objects.order_by('-score', 'date')[:10]
    
    return render(request, 'result.html', {
        'score': score,
        'total': total,
        'leaderboard': leaderboard
    })


