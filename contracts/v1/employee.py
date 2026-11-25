"""Employee contract using fields present in Lucca, IFS and Progessi source schemas."""

from datetime import date

from pydantic import Field

from contracts.v1.base import CommonModel


class Employee(CommonModel):
    lucca_id: int | str | None = Field(
        default=None,
        alias="id",
        json_schema_extra={"source": "mocks/specs/lucca/real_openapi_specs.json: employee.id"},
    )
    remote_id: str | None = Field(
        default=None,
        alias="remoteId",
        json_schema_extra={
            "source": "mocks/specs/lucca/real_openapi_specs.json: employee.remoteId"
        },
    )
    employee_number: str | None = Field(
        default=None,
        alias="employeeNumber",
        json_schema_extra={
            "source": "mocks/specs/lucca/real_openapi_specs.json: employee.employeeNumber"
        },
    )
    given_name: str | None = Field(
        default=None,
        alias="givenName",
        json_schema_extra={
            "source": "mocks/specs/lucca/real_openapi_specs.json: employee.givenName; IFS PersonInfoSet.FirstName; OFBiz Person.firstName"
        },
    )
    family_name: str | None = Field(
        default=None,
        alias="familyName",
        json_schema_extra={
            "source": "mocks/specs/lucca/real_openapi_specs.json: employee.familyName; IFS PersonInfoSet.LastName; OFBiz Person.lastName"
        },
    )
    email: str | None = Field(
        default=None,
        json_schema_extra={"source": "mocks/specs/lucca/real_openapi_specs.json: employee.email"},
    )
    phone_number: str | None = Field(
        default=None,
        alias="phoneNumber",
        json_schema_extra={
            "source": "mocks/specs/lucca/real_openapi_specs.json: employee.phoneNumber"
        },
    )
    status: str | None = Field(
        default=None,
        json_schema_extra={"source": "mocks/specs/lucca/real_openapi_specs.json: employee.status"},
    )
    company_id: str | None = Field(
        default=None,
        alias="CompanyId",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: EmployeesHandling/CompanyPersonSet"
        },
    )
    emp_no: str | None = Field(
        default=None,
        alias="EmpNo",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: EmployeesHandling/CompanyPersonSet"
        },
    )
    person_id: str | None = Field(
        default=None,
        alias="PersonId",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: EmployeesHandling/CompanyPersonSet"
        },
    )
    date_of_employment: date | None = Field(
        default=None,
        alias="DateOfEmployment",
        json_schema_extra={
            "source": "mocks/specs/ifs/SOURCE.md: EmployeesHandling/CompanyPersonSet"
        },
    )
