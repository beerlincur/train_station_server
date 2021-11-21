from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Ticket(BaseModel):
    ticket_id: int
    road_id: int
    departure_station_id: int
    arrival_station_id: int
    car_number: int
    is_bought: bool
    is_in_train: bool


class ApplicationResponseFeed(Application):
    courier: Optional[Profile]
    samples: Optional[List[Sample]]
    results: Optional[List[ResultResponse]]
    markers: Optional[List[MarkerAssistantResponse]]


class ApplicationResponse(BaseModel):
    id: int
    number: str
    address: str
    profile: Profile
    courier: Optional[Profile]
    laboratory: Optional[Laboratory]
    research_object: ResearchObjectResponse
    complex: Optional[ComplexResponse]
    markers: List[MarkerResponse]
    samples: List[Sample]
    results: List[ResultResponse]
    sampling: SamplingType
    payment: PaymentType
    price: int
    period: int
    status: ApplicationStatusType
    created_at: datetime
    updated_at: datetime
    couriers_comment: Optional[str]
    samples_inspection_result: Optional[str]
    samples_storage_conditions: Optional[str]
    qr_code: str
    inspection_doc: Optional[str]
    sampling_result: Optional[str]
    identification_signs: Optional[str]
    samples_taking_conditions: Optional[str]
    is_sampling_report_submitted: bool
    analyzers: Optional[str]
    drafter: Optional[str]
    lab_manager: Optional[str]
    is_results_submitted: bool
    sampling_report_submit_time: Optional[datetime]


class ApplicationRequest(BaseModel):
    address: str
    email: EmailStr
    research_object_id: int
    complex_id: Optional[int]
    markers_to_add: Optional[List[int]]
    markers_to_delete: Optional[List[int]]
    laboratory_id: Optional[int]
    sampling: SamplingType
    payment: PaymentType
    first_name: str
    last_name: str
    middle_name: Optional[str]
    phone: str
    role: ProfileRoleType
    tax_number: Optional[int]
    reg_number: Optional[int]
    company_name: Optional[str]

    def update_profile(self, profile: Profile) -> None:
        profile.first_name = self.first_name
        profile.last_name = self.last_name
        profile.email = self.email
        if self.middle_name:
            profile.middle_name = self.middle_name
        profile.phone = self.phone
        profile.role = self.role
        if self.tax_number:
            profile.tax_number = self.tax_number
        if self.reg_number:
            profile.reg_number = self.reg_number
        if self.company_name:
            profile.company_name = self.company_name


class ApplicationAdminUpdateRequest(BaseModel):
    address: Optional[str]
    research_object_id: Optional[int]
    complex_id: Optional[int]
    laboratory_id: Optional[int]
    courier_id: Optional[int]
    markers_to_add: Optional[List[int]]
    markers_to_delete: Optional[List[int]]
    sampling: Optional[SamplingType]
    payment: Optional[PaymentType]
    status: Optional[ApplicationStatusType]
    couriers_comment: Optional[str]
    samples_inspection_result: Optional[str]
    samples_storage_conditions: Optional[str]
    inspection_doc: Optional[str]
    sampling_result: Optional[str]
    identification_signs: Optional[str]
    samples_taking_conditions: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    role: Optional[ProfileRoleType]
    tax_number: Optional[int]
    reg_number: Optional[int]
    company_name: Optional[str]
    is_sampling_report_submitted: Optional[bool]
    analyzers: Optional[str]
    drafter: Optional[str]
    lab_manager: Optional[str]
    is_results_submitted: Optional[bool]

    def update_application(self, application: Application) -> None:
        if self.address:
            application.address = self.address
        if self.research_object_id:
            application.research_object_id = self.research_object_id
        if self.complex_id:
            application.complex_id = self.complex_id
        if self.laboratory_id:
            application.laboratory_id = self.laboratory_id
        if self.courier_id:
            application.courier_id = self.courier_id
        if self.sampling:
            application.sampling = self.sampling
        if self.payment:
            application.payment = self.payment
        if self.status:
            application.status = self.status
        if self.couriers_comment:
            application.couriers_comment = self.couriers_comment
        if self.samples_inspection_result:
            application.samples_inspection_result = self.samples_inspection_result
        if self.samples_storage_conditions:
            application.samples_storage_conditions = self.samples_storage_conditions
        if self.inspection_doc:
            application.inspection_doc = self.inspection_doc
        if self.sampling_result:
            application.sampling_result = self.sampling_result
        if self.identification_signs:
            application.identification_signs = self.identification_signs
        if self.samples_taking_conditions:
            application.samples_taking_conditions = self.samples_taking_conditions
        if self.is_sampling_report_submitted is not None:
            application.is_sampling_report_submitted = self.is_sampling_report_submitted
        if self.analyzers:
            application.analyzers = self.analyzers
        if self.drafter:
            application.drafter = self.drafter
        if self.lab_manager:
            application.lab_manager = self.lab_manager
        if self.is_results_submitted is not None:
            application.is_results_submitted = self.is_results_submitted
        application.updated_at = datetime.now()

    def update_profile(self, profile: Profile) -> None:
        if self.first_name:
            profile.first_name = self.first_name
        if self.last_name:
            profile.last_name = self.last_name
        if self.email:
            profile.email = self.email
        if self.middle_name:
            profile.middle_name = self.middle_name
        if self.phone:
            profile.phone = self.phone
        if self.role:
            profile.role = self.role
        if self.tax_number:
            profile.tax_number = self.tax_number
        if self.reg_number:
            profile.reg_number = self.reg_number
        if self.company_name:
            profile.company_name = self.company_name


class ApplicationClientUpdateRequest(BaseModel):
    address: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    tax_number: Optional[int]
    reg_number: Optional[int]
    company_name: Optional[str]

    def update_application(self, application: Application) -> None:
        if self.address:
            application.address = self.address
        application.updated_at = datetime.now()

    def update_profile(self, profile: Profile) -> None:
        if self.first_name:
            profile.first_name = self.first_name
        if self.last_name:
            profile.last_name = self.last_name
        if self.email:
            profile.email = self.email
        if self.middle_name:
            profile.middle_name = self.middle_name
        if self.phone:
            profile.phone = self.phone
        if self.tax_number:
            profile.tax_number = self.tax_number
        if self.reg_number:
            profile.reg_number = self.reg_number
        if self.company_name:
            profile.company_name = self.company_name


class ApplicationCourierUpdateRequest(BaseModel):
    address: Optional[str]
    couriers_comment: Optional[str]
    samples_inspection_result: Optional[str]
    samples_storage_conditions: Optional[str]
    inspection_doc: Optional[str]
    sampling_result: Optional[str]
    identification_signs: Optional[str]
    samples_taking_conditions: Optional[str]

    def update_application(self, application: Application) -> None:
        if self.address:
            application.address = self.address
        if self.couriers_comment:
            application.couriers_comment = self.couriers_comment
        if self.samples_inspection_result:
            application.samples_inspection_result = self.samples_inspection_result
        if self.samples_storage_conditions:
            application.samples_storage_conditions = self.samples_storage_conditions
        if self.inspection_doc:
            application.inspection_doc = self.inspection_doc
        if self.sampling_result:
            application.sampling_result = self.sampling_result
        if self.identification_signs:
            application.identification_signs = self.identification_signs
        if self.samples_taking_conditions:
            application.samples_taking_conditions = self.samples_taking_conditions
        application.updated_at = datetime.now()


class ApplicationLaboratoryUpdateRequest(BaseModel):
    analyzers: Optional[str]
    drafter: Optional[str]
    lab_manager: Optional[str]
    is_results_submitted: Optional[bool]

    def update_application(self, application: Application) -> None:
        if self.analyzers:
            application.analyzers = self.analyzers
        if self.drafter:
            application.drafter = self.drafter
        if self.lab_manager:
            application.lab_manager = self.lab_manager
        if self.is_results_submitted is not None:
            application.is_results_submitted = self.is_results_submitted


class ApplicationUpdateStatusRequest(BaseModel):
    status: str

    def update_application(self, application: Application) -> None:
        application.status = self.status


class ApplicationUpdateIsSamplingReportSubmitted(BaseModel):
    is_sampling_report_submitted: bool


class ApplicationUpdateIsResultsSubmitted(BaseModel):
    is_results_submitted: bool