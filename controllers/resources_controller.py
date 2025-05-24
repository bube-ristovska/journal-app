from flask import Blueprint, render_template, request, jsonify
from models.database import db
from models.resources import CopingStrategy, CrisisResource, EducationalContent

resources_bp = Blueprint('resources', __name__, url_prefix='/resources')


@resources_bp.route('/')
def index():
    return render_template('resources/index.html')


@resources_bp.route('/crisis')
def crisis():
    resources = CrisisResource.query.filter_by(country='Macedonia').all()
    emergency_resources = CrisisResource.query.filter_by(is_emergency=True).all()

    # Default crisis resources for Macedonia
    if not resources:
        default_resources = [
            {
                'name': 'Национална линија за превенција на самоубиство',
                'phone': '02 3061-661',
                'description': '...',
                'instructions': '...',
                'benefits': '...'
            },
            ...
        ]

        for resource_data in default_resources:
            resource = CrisisResource(**resource_data)
            db.session.add(resource)
        db.session.commit()

        resources = CrisisResource.query.filter_by(country='Macedonia').all()

    return render_template('resources/crisis.html', resources=resources, emergency_resources=emergency_resources)

@resources_bp.route('/education')
def education():
    content = EducationalContent.query.filter_by(age_group='teenagers').all()

    # Default educational content
    if not content:
        default_content = [
            {
                'title': 'Што е анксиозност?',
                'category': 'Анксиозност',
                'age_group': 'teenagers',
                'reading_time': 5,
                'content': '''Анксиозноста е нормална емоција која ја чувствуваат сите луѓе. Таа се јавува кога нашиот мозок мисли дека сме во опасност.

**Симптоми на анксиозност:**
- Брзо чукање на срцето
- Потење
- Треперење
- Тешко дишење
- Мисли кои се вртат во круг

**Како да се справиш:**
- Практикувај техники за дишење
- Зборувај со доверлив човек
- Ограничи го кофеинот
- Редовно вежбај
- Доволно спиј

Запомни: Анксиозноста е лечлива и со правилна помош можеш да ја контролираш.''',
                'tags': 'анксиозност,стрес,справување'
            },
            {
                'title': 'Важноста на спиењето за тинејџери',
                'category': 'Спиење',
                'age_group': 'teenagers',
                'reading_time': 4,
                'content': '''Тинејџерите треба 8-10 часа спиење секоја ноќ за оптимално здравје и развој.

**Зошто е важно спиењето:**
- Помага во консолидација на меморијата
- Поддржува физички раст
- Јакне имунитетот
- Подобрува расположението
- Зголемува концентрацијата

**Совети за подобар сон:**
- Воспостави рутина пред спиење
- Избегнувај екрани 1 час пред спиење
- Создај мирна атмосфера во спалната
- Ограничи го кофеинот попладне
- Редовно се излегувај на сонце

Добриот сон е инвестиција во твоето ментално и физичко здравје.''',
                'tags': 'спиење,здравје,рутина'
            },
            {
                'title': 'Социјални медиуми и ментално здравје',
                'category': 'Социјални медиуми',
                'age_group': 'teenagers',
                'reading_time': 6,
                'content': '''Социјалните медиуми можат да влијаат на нашето ментално здравје на позитивен и негативен начин.

**Негативни ефекти:**
- Споредување со други
- FOMO (страв од пропуштање)
- Кибер малтретирање
- Нарушено спиење
- Намалена самодоверба

**Позитивни ефекти:**
- Поврзување со пријатели
- Наоѓање заедници со слични интереси
- Пристап до образовни содржини
- Креативно изразување

**Здрави навики:**
- Ограничи го времето на екранот
- Не следи профили кои те прават да се чувствуваш лошо
- Користи функции за благосостојба
- Прави редовни паузи
- Комуницирај отворено со родителите

Запомни: Ти контролираш како ги користиш социјалните медиуми.''',
                'tags': 'социјални медиуми,дигитално здравје,самодоверба'
            }
        ]

        for content_data in default_content:
            article = EducationalContent(**content_data)
            db.session.add(article)
        db.session.commit()

        content = EducationalContent.query.filter_by(age_group='teenagers').all()

    categories = list(set([c.category for c in content]))
    return render_template('resources/education.html', content=content, categories=categories)