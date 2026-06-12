export default function MessageBubble({
  message,
  onMentorRequest
  }) {
  
  const {
  role,
  text,
  suggest_mentor
  } = message;
  
  
  if (role === "system") {
  
  return (
  
    <div className="flex justify-center">
  
      <div
        className="
          bg-yellow-500/10
          border
          border-yellow-500/30
          text-yellow-300
          px-4
          py-2
          rounded-full
          text-sm
        "
      >
        {text}
      </div>
  
    </div>
  
  );
  
  
  }
  
  if (role === "user") {
  
  return (
  
    <div className="flex justify-end">
  
      <div
        className="
          max-w-[75%]
          bg-indigo-600
          text-white
          px-4
          py-3
          rounded-2xl
          rounded-br-md
          whitespace-pre-wrap
          break-words
          shadow
        "
      >
        {text}
      </div>
  
    </div>
  
  );
  
  
  }

  
  if (role === "mentor") {
  
  
  return (
  
    <div className="flex gap-3">
  
      <div
        className="
          w-10
          h-10
          rounded-full
          bg-emerald-600
          flex
          items-center
          justify-center
          text-white
          font-semibold
          shrink-0
        "
      >
        M
      </div>
  
      <div className="max-w-[80%]">
  
        <div
          className="
            text-xs
            text-emerald-400
            mb-1
            font-medium
          "
        >
          Mentor
        </div>
  
        <div
          className="
            bg-emerald-500/10
            border
            border-emerald-500/20
            text-zinc-100
            px-4
            py-3
            rounded-2xl
            rounded-tl-md
            whitespace-pre-wrap
            break-words
          "
        >
          {text}
        </div>
  
      </div>
  
    </div>
  
  );
  
  
  }
  
  
  return (
  

  <div className="flex gap-3">
  
    <div
      className="
        w-10
        h-10
        rounded-full
        bg-indigo-600
        flex
        items-center
        justify-center
        text-white
        shrink-0
      "
    >
    </div>
  
    <div className="max-w-[80%]">
  
      <div
        className="
          text-xs
          text-zinc-400
          mb-1
          font-medium
        "
      >
        DoDo
      </div>
  
      <div
        className="
          bg-zinc-800
          border
          border-zinc-700
          text-zinc-100
          px-4
          py-3
          rounded-2xl
          rounded-tl-md
          whitespace-pre-wrap
          break-words
          leading-relaxed
        "
      >
        {text}
      </div>
  
      {suggest_mentor && (
  
        <button
          onClick={onMentorRequest}
          className="
            mt-3
            bg-emerald-600
            hover:bg-emerald-500
            text-white
            px-4
            py-2
            rounded-xl
            text-sm
            transition
          "
        >
          🎓 Kết nối Mentor
        </button>
  
      )}
  
    </div>
  
  </div>
  
  );
  
  }
  