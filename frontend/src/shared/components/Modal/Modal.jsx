import "./Modal.scss";
import ButtonLink from "../ButtonLink/ButtonLink";

function Modal({ children, onClose }) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <button type="button" className="modal__close" onClick={onClose}>
          X
        </button>
        {children}
      </div>
    </div>
  );
}

export default Modal;
