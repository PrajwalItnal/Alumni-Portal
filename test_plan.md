# Alumni Portal Comprehensive Test Plan

This document outlines the testing strategy for the Alumni Portal to ensure all functions work correctly, data validation is robust, and role-based access control is properly implemented.

## User Roles and Credentials
(Based on `setup_test_users.py`)

| Role | Register ID | Password | Name |
| :--- | :--- | :--- | :--- |
| **Admin** | `ADM001` | `admin123` | Test Admin |
| **Alumni** | `ALU001` | `alumni123` | Test Alumni |
| **Student** | `STD001` | `student123` | Test Student |

## Functional Test Checklist

### 1. Common Functions (All Roles)
- [ ] **Home Page Navigation**: Correct redirects based on role.
- [ ] **Logout**: Session clearing and redirection to login.
- [ ] **Change Password**: Validation (length >= 8, match) and functional update.
- [ ] **Profile View**: Correct display of role-specific information.

### 2. Admin Specific Functions
- [ ] **Student Registration**: 
    - [ ] Bulk upload (Excel/CSV)
    - [ ] Validation (Email domain, Phone format, Gender, Unique IDs)
    - [ ] Error report generation for failed rows.
- [ ] **Manage Departments**:
    - [ ] Add Department (Validation: No empty, Unique name)
    - [ ] Edit Department (Updates linked students)
    - [ ] Delete Department (Clears links in students)
- [ ] **Change User Email/Password**: Admin-only tool for account recovery.
- [ ] **Convert Students to Alumni**: Automatic conversion for current year graduates.

### 3. Events Management
- [ ] **View Events**: Listed by most recent.
- [ ] **Create Event** (Admin/Alumni):
    - [ ] Validation: Date (tomorrow to 60 days), Image (size < 2MB, format), Text (Alpha only).
- [ ] **Edit Event**: Only owner or Admin can edit.
- [ ] **Delete Event**: Only owner or Admin can delete.

### 4. Achievements Management
- [ ] **View Achievements**: Sequential display.
- [ ] **Create Achievement** (Admin/Alumni):
    - [ ] Validation: Text (Alpha only), File (PDF/Image/Doc, size < 5MB), Description (> 5 words).
- [ ] **Edit Achievement**: Ownership check.
- [ ] **Delete Achievement**: Ownership check.

### 5. Donations Management
- [ ] **View Donations**: All roles.
- [ ] **Record Donation** (Admin/Alumni):
    - [ ] Validation: Amount (min 1000), Description (Alpha only).
- [ ] **Edit Donation**: Ownership check.
- [ ] **Delete Donation**: Ownership check.

### 6. Jobs Management
- [ ] **View Jobs**: Student-specific skill matching and sorting.
- [ ] **Post Job** (Admin/Alumni):
    - [ ] Validation: Text (Alpha only), Salary (Positive number), Description (> 5 words), Date (Future, < 2 months), URL format.
- [ ] **Filter Jobs**: Title and Location search.
- [ ] **Edit/Delete Job**: Ownership check.

### 7. Internship Management
- [ ] **View Internships**: Filterable.
- [ ] **Post Internship** (Admin/Alumni):
    - [ ] Validation: Text (Alpha only), Stipend (Positive), Date (Future, < 2 months), Description (> 5 words).
- [ ] **Filter Internship**: Search with specific location match logic.
- [ ] **Edit/Delete Internship**: Ownership check.

### 8. Directories & Career Track
- [ ] **Alumni Directory**: Search by Name, Dept, Year, Company, Job, Degree.
- [ ] **Student Directory** (Admin/Alumni Only): Search by Name, ID, Dept, Year.
- [ ] **Alumni Career Track**: Comprehensive view of alumni progress.
- [ ] **Career Track Download**: CSV export of the filtered/full list.

---

## Data Validation Edge Cases to Test
- Empty fields in required forms.
- Invalid date ranges (Past dates, too far in future).
- File size and format violations (Large images, wrong extensions).
- Text fields with special characters (Testing `is_valid_text`).
- Numerical range violations (Donation < 1000, negative salaries).
- Duplicate names/IDs in registration and department management.
