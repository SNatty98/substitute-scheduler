from ..models import Assignment, Application


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
