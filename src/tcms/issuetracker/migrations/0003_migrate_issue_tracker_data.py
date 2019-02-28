# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-03 16:08
from django.db import migrations

from tcms.issuetracker.models import CredentialTypes


def migrate_to_issue_tracker(apps, schema_editor):
    TestCaseBugSystem = apps.get_model('testcases', 'TestCaseBugSystem')
    TestCaseBug = apps.get_model('testcases', 'TestCaseBug')
    IssueTracker = apps.get_model('issuetracker', 'IssueTracker')
    IssueTrackerProduct = apps.get_model('issuetracker', 'IssueTrackerProduct')
    ProductIssueTrackerRelationship = apps.get_model(
        'issuetracker', 'ProductIssueTrackerRelationship')
    Issue = apps.get_model('issuetracker', 'Issue')
    Product = apps.get_model('management', 'Product')

    issue_tracker_cred_type = {
        'Bugzilla': CredentialTypes.UserPwd.name,
        'JIRA': CredentialTypes.NoNeed.name,
    }

    existing_products = Product.objects.all()

    for bug_system in TestCaseBugSystem.objects.all():
        credential_type = issue_tracker_cred_type[bug_system.name]
        tracker_product = IssueTrackerProduct.objects.get(name=bug_system.name)

        issue_tracker = IssueTracker.objects.create(
            name=bug_system.name,
            description=bug_system.description,
            service_url='',
            api_url='',
            issue_url_fmt=bug_system.url_reg_exp,
            validate_regex=bug_system.validate_reg_exp,
            credential_type=credential_type,
            tracker_product=tracker_product)

        for product in existing_products:
            ProductIssueTrackerRelationship.objects.create(
                product=product, issue_tracker=issue_tracker)

        for bug in TestCaseBug.objects.filter(bug_system=bug_system):
            Issue.objects.create(
                issue_key=bug.bug_id,
                summary=bug.summary,
                description=bug.description,
                tracker=issue_tracker,
                case=bug.case,
                case_run=bug.case_run)

    TestCaseBug.objects.all().delete()
    TestCaseBugSystem.objects.all().delete()


# In practice, it should make no sense to migrate legacy bug system and bugs
# back to original value. But, these code are also provided for the consistent
# migration. It works but Nitrate does not work with the original bug system
# and bugs data any more.


def restore_back_to_original_bug_systems(apps, schema_editor):
    TestCaseBugSystem = apps.get_model('testcases', 'TestCaseBugSystem')
    TestCaseBug = apps.get_model('testcases', 'TestCaseBug')
    IssueTracker = apps.get_model('issuetracker', 'IssueTracker')
    Issue = apps.get_model('issuetracker', 'Issue')
    ProductIssueTrackerRelationship = apps.get_model(
        'issuetracker', 'ProductIssueTrackerRelationship')

    for tracker in IssueTracker.objects.all():
        bug_system = TestCaseBugSystem.objects.create(
            name=tracker.name,
            description=tracker.description,
            url_reg_exp=tracker.issue_url_fmt,
            validate_reg_exp=tracker.validate_regex)
        for issue in tracker.issues.all():
            TestCaseBug.objects.create(
                bug_id=issue.issue_key,
                summary=issue.summary,
                description=issue.description,
                bug_system=bug_system,
                case=issue.case,
                case_run=issue.case_run)

    Issue.objects.all().delete()
    ProductIssueTrackerRelationship.objects.all().delete()
    IssueTracker.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0002_add_issue_tracker_products'),
    ]

    operations = [
        migrations.RunPython(
            migrate_to_issue_tracker,
            restore_back_to_original_bug_systems
        ),
    ]
