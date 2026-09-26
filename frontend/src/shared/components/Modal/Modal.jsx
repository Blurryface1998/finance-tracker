import Card from "../Card/Card";
import "./Modal.scss";

function Modal({ children, onClose }) {
  return (
    <div className={onClose ? "modal-overlay" : "modal-overlay open"}>
      <Card className="modal">
        <button type="button" className="modal__close" onClick={onClose}>
          X
        </button>
        {children}
      </Card>
    </div>
  );
}

export default Modal;
