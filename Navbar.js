import { Link } from 'react-scroll'
import './Navbar.css'

const Navbar = () => {
  return (
    <div className='nav'>
        <div className='nav-logo'>Formify</div>
        <ul className='nav-menu'>
          <li className='nav-contact2'><Link to='hero' smooth={true} offset={-60} duration={500}>Home</Link></li>
          <li className='nav-contact2'><Link to='about' smooth={true} offset={30} duration={500}>About</Link></li>
          <li className='nav-contact2'><Link to='FileUpload' smooth={true} offset={0} duration={500}>Upload</Link></li>
          <li className='nav-contact'><Link to='contact' smooth={true} offset={0} duration={500}>Contact</Link></li>
        </ul>
    </div>
  )
}

export default Navbar
