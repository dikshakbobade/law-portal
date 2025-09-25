from django.core.management.base import BaseCommand
from laws.models import Category, Law
from datetime import datetime

class Command(BaseCommand):
    help = 'Load sample law data'
    
    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            'Criminal', 'Civil', 'Constitutional', 'Personal/Family',
            'Corporate/Commercial', 'Labour/Employment', 'Property/Land',
            'Taxation', 'Environmental', 'Cyber/Technology'
        ]
        
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'{cat_name} laws and regulations'}
            )
            if created:
                self.stdout.write(f'Created category: {cat_name}')
        
        # Create sample laws
        criminal_cat = Category.objects.get(name='Criminal')
        Law.objects.get_or_create(
            title='Indian Penal Code - Section 302',
            defaults={
                'category': criminal_cat,
                'summary': 'Punishment for murder',
                'full_text': 'Whoever commits murder shall be punished with death, or imprisonment for life.',
                'act_number': 'IPC 1860',
                'section': '302',
                'keywords': 'murder, punishment, death penalty',
                'jurisdiction': 'India',
                'enacted_date': datetime(1860, 10, 6).date(),
            }
        )
        
        civil_cat = Category.objects.get(name='Civil')
        Law.objects.get_or_create(
            title='Contract Act - Section 10',
            defaults={
                'category': civil_cat,
                'summary': 'What agreements are contracts',
                'full_text': 'All agreements are contracts if they are made by free consent of parties.',
                'act_number': 'Contract Act 1872',
                'section': '10',
                'keywords': 'contract, agreement, consent',
                'jurisdiction': 'India',
                'enacted_date': datetime(1872, 4, 25).date(),
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))