from ..models import Assignment, Application
from .postcode_service import PostcodeService


class AssignmentService:

    @staticmethod
    def select_substitute(assignment, application):
        if application.assignment != assignment:
            raise ValueError("Application does not belong to this assignment.")

        if assignment.status == assignment.FILLED:
            raise ValueError("Assignment is already filled.")

        assignment.selected_substitute = application.substitute
        assignment.status = Assignment.FILLED
        assignment.save()

        application.status = Application.ACCEPTED
        application.save()

        assignment.applications.exclude(
            id=application.id).update(status=Application.REJECTED)

        return assignment

    def create_with_postcode_lookup(school_name, school_postcode, date, start_time,
                                    end_time, subject, created_by, year_group='', notes=''):
        try:
            postcode_data = PostcodeService.lookup(school_postcode)
        except ValueError as e:
            raise ValueError(f"Invalid school postcode: {str(e)}")

        # Create assignment with coordinates
        assignment = Assignment.objects.create(
            school_name=school_name,
            school_postcode=postcode_data['postcode'],  # Formatted postcode
            school_latitude=postcode_data['latitude'],
            school_longitude=postcode_data['longitude'],
            date=date,
            start_time=start_time,
            end_time=end_time,
            subject=subject,
            year_group=year_group,
            notes=notes,
            created_by=created_by,
            status=Assignment.OPEN
        )

        return assignment
