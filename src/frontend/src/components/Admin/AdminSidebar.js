//Packages
import { Link } from 'react-router-dom';
//Assets
function AdminSidebar(props){
    return(
        <div className="list-group">
            <Link to="/admin-page/dashboard" className="list-group-item list-group-item-action active">Dashboard</Link>
            <Link to="/admin-page/customers" className="list-group-item list-group-item-action ">Customers</Link>
            <Link to="/admin-page/vendors" className="list-group-item list-group-item-action ">Vendors</Link>
            <Link to="/admin-page/report" className="list-group-item list-group-item-action ">Reports</Link>
            <Link to='/admin-page/logout' className="list-group-item list-group-item-action text-danger ">Logout</Link>
        </div>


    );
}

export default AdminSidebar;