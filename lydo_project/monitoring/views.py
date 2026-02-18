import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Youth, Barangay
from better_profanity import profanity

# Load profanity filter
profanity.load_censor_words()
custom_bad_words = ['gago', 'puta', 'yawa', 'piste']
profanity.add_censor_words(custom_bad_words)

# --- AUTH VIEWS ---

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        # Create user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        # Auto-login after register
        login(request, user)
        return JsonResponse({'message': 'Registered and logged in successfully'})
    return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'username': user.username})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'POST method required'}, status=405)

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

def user_info_view(request):
    """Check if user is logged in"""
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True, 'username': request.user.username})
    return JsonResponse({'is_authenticated': False}, status=401)

# --- APP VIEWS ---

@ensure_csrf_cookie
def index(request):
    """Serves the frontend HTML page"""
    return render(request, 'index.html')

@csrf_exempt
def youth_api(request):
    """Handles Listing (GET) and Full Profile CRUD"""

    # 1. GET: List all youths
    if request.method == 'GET':
        youths = Youth.objects.all().select_related('barangay') # Optimized query
        data = []
        for y in youths:
            data.append({
                'id': y.id,
                'name': y.name,
                'age': y.age,
                'sex': y.sex,
                'barangay_name': y.barangay.name, # Helper for display
                'barangay_id': y.barangay.id,     # Helper for filtering
                'education_level': y.education_level,
                'full_data': { 
                    'birthdate': str(y.birthdate) if y.birthdate else '',
                    'civil_status': y.civil_status,
                    'religion': y.religion,
                    'purok': y.purok,
                    'barangay_id': y.barangay.id,
                    'email': y.email,
                    'contact_number': y.contact_number,
                    'is_in_school': y.is_in_school,
                    'is_osy': y.is_osy,
                    'osy_willing_to_enroll': y.osy_willing_to_enroll,
                    'osy_program_type': y.osy_program_type,
                    'osy_reason_no_enroll': y.osy_reason_no_enroll,
                    'is_working_youth': y.is_working_youth,
                    'is_pwd': y.is_pwd,
                    'disability_type': y.disability_type,
                    'has_specific_needs': y.has_specific_needs,
                    'specific_needs_condition': y.specific_needs_condition,
                    'is_ip': y.is_ip,
                    'tribe_name': y.tribe_name,
                    'is_muslim': y.is_muslim,
                    'muslim_group': y.muslim_group,
                    'course': y.course,
                    'school_name': y.school_name,
                    'is_scholar': y.is_scholar,
                    'scholarship_program': y.scholarship_program,
                    'work_status': y.work_status,
                    'registered_voter_sk': y.registered_voter_sk,
                    'registered_voter_national': y.registered_voter_national,
                    'voted_last_sk': y.voted_last_sk,
                    'attended_kk_assembly': y.attended_kk_assembly,
                    'kk_assembly_times': y.kk_assembly_times,
                    'kk_assembly_no_reason': y.kk_assembly_no_reason,
                    'is_4ps': y.is_4ps,
                    'number_of_children': y.number_of_children,
                }
            })
        return JsonResponse(data, safe=False)

    # ... (Keep the rest of the Authentication check and POST/PUT/DELETE logic exactly the same) ...
    # Copy the previous POST/PUT/DELETE code here if you deleted it.
    
    # 2. AUTH CHECK
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized. Please login.'}, status=401)

    # 3. POST/PUT Logic (Same as before)
    if request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
           
           
            if profanity.contains_profanity(data.get('name', '')):
                return JsonResponse({'error': 'Profanity detected in name.'}, status=400)

            barangay = get_object_or_404(Barangay, id=data.get('barangay_id'))
            def get_bool(key): return data.get(key, False)
            
            fields = {
                'name': data.get('name'),
                'birthdate': data.get('birthdate') or None,
                'sex': data.get('sex'),
                'civil_status': data.get('civil_status'),
                'religion': data.get('religion'),
                'purok': data.get('purok'),
                'barangay': barangay,
                'email': data.get('email'),
                'contact_number': data.get('contact_number'),
                'is_in_school': get_bool('is_in_school'),
                'is_osy': get_bool('is_osy'),
                'osy_willing_to_enroll': get_bool('osy_willing_to_enroll'),
                'osy_program_type': data.get('osy_program_type'),
                'osy_reason_no_enroll': data.get('osy_reason_no_enroll'),
                'is_working_youth': get_bool('is_working_youth'),
                'is_pwd': get_bool('is_pwd'),
                'disability_type': data.get('disability_type'),
                'has_specific_needs': get_bool('has_specific_needs'),
                'specific_needs_condition': data.get('specific_needs_condition'),
                'is_ip': get_bool('is_ip'),
                'tribe_name': data.get('tribe_name'),
                'is_muslim': get_bool('is_muslim'),
                'muslim_group': data.get('muslim_group'),
                'education_level': data.get('education_level'),
                'course': data.get('course'),
                'school_name': data.get('school_name'),
                'is_scholar': get_bool('is_scholar'),
                'scholarship_program': data.get('scholarship_program'),
                'work_status': data.get('work_status'),
                'registered_voter_sk': get_bool('registered_voter_sk'),
                'registered_voter_national': get_bool('registered_voter_national'),
                'voted_last_sk': get_bool('voted_last_sk'),
                'attended_kk_assembly': get_bool('attended_kk_assembly'),
                'kk_assembly_times': int(data.get('kk_assembly_times') or 0),
                'kk_assembly_no_reason': data.get('kk_assembly_no_reason'),
                'is_4ps': get_bool('is_4ps'),
                'number_of_children': int(data.get('number_of_children') or 0),
            }

            if request.method == 'POST':
                Youth.objects.create(**fields)
                return JsonResponse({'message': 'Youth added successfully'})
            elif request.method == 'PUT':
                youth = get_object_or_404(Youth, id=data.get('id'))
                for key, value in fields.items(): setattr(youth, key, value)
                youth.save()
                return JsonResponse({'message': 'Updated successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            youth = get_object_or_404(Youth, id=data.get('id'))
            youth.delete()
            return JsonResponse({'message': 'Deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)