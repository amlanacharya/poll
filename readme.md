# Grip the Facts

## Overview

"Grip the Facts" is a polling application built using Streamlit, allowing users to participate in polls and view results in real-time. The application features two main roles: Students and Admins. Students can register, vote in polls, and view results, while Admins can manage polls and view student data.

## Features

- **User Registration**: Students can register with their name, mobile number, and email.
- **Voting System**: Students can participate in active polls and submit their votes.
- **Admin Dashboard**: Admins can create, activate, deactivate, and delete polls, as well as view voting results.
- **Real-time Results**: Poll results are updated in real-time, providing immediate feedback to users.
- **Data Export**: Admins can export student data as a CSV file.

## Technologies Used

- **Streamlit**: For building the web application.
- **SQLite**: For database management.
- **Plotly**: For visualizing poll results.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amlanacharya/mypoll.git
   cd mypoll
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## File Structure

```

## Usage

1. **For Students**:
   - Navigate to the Student page to register and participate in polls.
   - View the results of the polls after voting.

2. **For Admins**:
   - Navigate to the Admin page to log in using the admin password.
   - Manage polls, view results, and export student data.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
