from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import Profile
from .utils import validate_password, validate_username, generate_otp


# ---------------- SIGNUP VIEW ----------------
def signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation checks
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'account/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'account/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'account/signup.html')

        # Password & username validation
        error = validate_username(username)
        if error:
            messages.error(request, error)
            return render(request, 'account/signup.html')
        error = validate_password(password, username)
        if error:
            messages.error(request, error)
            return render(request, 'account/signup.html')

        # Validate phone
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Enter a valid 10-digit phone number")
            return render(request, 'account/signup.html')

        # Store data temporarily in session
        request.session['signup_data'] = {
            'full_name': full_name,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password
        }

        # Generate OTP
        otp = generate_otp()
        request.session['signup_otp'] = otp
        request.session['otp_created_at'] = timezone.now().isoformat()

        # Send OTP email
        send_mail(
            subject="Email Verification OTP",
            message=f"""
Hello {full_name},

Your OTP for email verification is: {otp}

This OTP is valid for 5 minutes.

Thank you,
Flower.in
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        return redirect('verify_otp_signup')


        

    return render(request, 'account/signup.html')


# ---------------- VERIFY OTP VIEW ----------------
def verify_otp_view(request):
    user_id = request.session.get('verify_user')
    if not user_id:
        messages.error(request, "Session expired. Please signup again.")
        return redirect('signup')

    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Please signup again.")
        return redirect('signup')

    if request.method == "POST":
        otp = request.POST.get('otp')

        # Check OTP expiry (5 minutes)
        if not profile.otp_created_at or timezone.now() - profile.otp_created_at > timedelta(minutes=5):
            messages.error(request, "OTP expired. Please resend OTP.")
            return redirect('verify_otp')

        if profile.email_otp == otp:
            # Mark email verified
            profile.is_email_verified = True
            profile.email_otp = ''
            profile.otp_created_at = None
            profile.save()

            # Activate the user so they can log in
            user = profile.user
            user.is_active = True
            user.save()

            request.session.pop('verify_user', None)  # remove OTP session

            return redirect('login')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'account/otpverify.html')



# ---------------- RESEND OTP VIEW ----------------
def resend_otp_view(request):
    user_id = request.session.get('verify_user')
    if not user_id:
        messages.error(request, "No user to verify")
        return redirect('signup')

    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Please signup again.")
        return redirect('signup')

    # 👉 Generate new OTP
    otp = generate_otp()
    profile.email_otp = otp
    profile.otp_created_at = timezone.now()
    profile.save()

    # 👉 EXACT LOCATION: SEND EMAIL HERE
    send_mail(
        subject="Email Verification OTP (Resent)",
        message=f"""
Hello,
    {profile.full_name},

    Your User ID is:  {profile.user.username}{profile.user.id}

    Your new OTP is: {otp}

    This OTP is valid for 5 minutes.

    Regards,

    Flower.in
    Santu Bera
                """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[profile.user.email],
        fail_silently=False
    )

    messages.success(request, "New OTP sent to your email")
    return redirect('verify_otp')


# ---------------- LOGIN VIEW ----------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            # Check if email is verified
            if not hasattr(user, 'profile') or not user.profile.is_email_verified:
                messages.error(request, "Please verify your email first")
                return redirect('login')

            # Log the user in
            login(request, user)

            # Redirect to home page
            return redirect('home')  # Make sure 'home' is the name of your home URL in urls.py
        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password")
            return redirect('login')  # <-- Important: redirect instead of render here

    return render(request, 'account/login.html')
# ---------------- LOGOUT VIEW ----------------
def logout_view(request):
    logout(request)
    return redirect('home')



def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            profile = user.profile
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect('forgot_password')

        otp = generate_otp()
        profile.email_otp = otp
        profile.otp_created_at = timezone.now()
        profile.save()

        send_mail(
            subject="Password Reset OTP",
            message=f"""
Hello ,
    {profile.full_name},
    Your User ID is:  {profile.user.username}{profile.user.id}

    Your OTP to reset password is: {otp}


    This OTP is valid for 5 minutes.
    
    Regards,

    Flower.in
    Santu Bera
                    """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        request.session['reset_user'] = user.id
        messages.success(request, "OTP sent to your email")
        return redirect('reset_verify_otp')

    return render(request, 'account/forgot_password.html')



def reset_verify_otp_view(request):
    user_id = request.session.get('reset_user')
    if not user_id:
        messages.error(request, "Session expired")
        return redirect('forgot_password')

    profile = Profile.objects.get(user_id=user_id)

    if request.method == "POST":
        otp = request.POST.get('otp')

        if timezone.now() - profile.otp_created_at > timedelta(minutes=5):
            messages.error(request, "OTP expired")
            return redirect('forgot_password')

        if profile.email_otp == otp:
            request.session['reset_verified'] = True
            return redirect('reset_password')

        messages.error(request, "Invalid OTP")

    return render(request, 'account/reset_otp.html')




def reset_password_view(request):
    if not request.session.get('reset_verified'):
        messages.error(request, "Unauthorized access")
        return redirect('forgot_password')

    user_id = request.session.get('reset_user')
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')

        error = validate_password(password, user.username)
        if error:
            messages.error(request, error)
            return redirect('reset_password')

        user.set_password(password)
        user.save()

        # Cleanup OTP
        profile = user.profile
        profile.email_otp = ''
        profile.otp_created_at = None
        profile.save()

        # Remove only reset-related session keys
        request.session.pop('reset_verified', None)
        request.session.pop('reset_user', None)

        # Auto-login
        login(request, user)

        messages.success(request, "Password reset successful! You are now logged in.")
        return redirect('home')

    return render(request, 'account/reset_password.html')
from django.contrib.auth import login

def verify_otp_signup_view(request):
    signup_data = request.session.get('signup_data')
    otp = request.session.get('signup_otp')
    otp_time = request.session.get('otp_created_at')

    if not signup_data or not otp or not otp_time:
        messages.error(request, "Session expired. Please signup again.")
        return redirect('signup')

    if request.method == "POST":
        user_otp = request.POST.get('otp')

        # Check OTP expiry
        if timezone.now() - timezone.datetime.fromisoformat(otp_time) > timedelta(minutes=5):
            messages.error(request, "OTP expired. Please signup again.")
            request.session.pop('signup_data', None)
            request.session.pop('signup_otp', None)
            request.session.pop('otp_created_at', None)
            return redirect('signup')

        if user_otp == otp:
            # Create user
            user = User.objects.create_user(
                username=signup_data['username'],
                email=signup_data['email'],
                password=signup_data['password']
            )
            user.is_active = True
            user.save()

            # Create profile
            Profile.objects.create(
                user=user,
                full_name=signup_data['full_name'],
                phone=signup_data['phone'],
                is_email_verified=True
            )

            # Cleanup session
            request.session.pop('signup_data', None)
            request.session.pop('signup_otp', None)
            request.session.pop('otp_created_at', None)

            # Auto-login the user
            login(request, user)

            messages.success(request, f"Signup successful! Welcome, {user.username}")
            return redirect('home')  # redirect to your homepage or dashboard

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'account/otpverify.html')
