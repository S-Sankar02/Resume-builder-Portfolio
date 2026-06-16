def autosave_resume(resume, data, db):
    resume.summary = data.get("summary", resume.summary)
    db.session.commit()