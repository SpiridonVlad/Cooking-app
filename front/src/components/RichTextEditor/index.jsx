import React, { useState, useEffect, useRef } from 'react'
import './index.css'

import ListItem from '@tiptap/extension-list-item'
import TextStyle from '@tiptap/extension-text-style'
import Image from '@tiptap/extension-image'
import StarterKit from '@tiptap/starter-kit'
import { EditorProvider, useCurrentEditor } from '@tiptap/react'

import { FiBold } from 'react-icons/fi'
import { FiUnderline } from 'react-icons/fi'
import { FiItalic } from 'react-icons/fi'
import { FiImage } from 'react-icons/fi'
import { GrTextAlignLeft } from 'react-icons/gr'
import { GoListOrdered } from 'react-icons/go'
import { GoListUnordered } from 'react-icons/go'
import { IoIosReturnLeft } from 'react-icons/io'
import { LuUndo } from 'react-icons/lu'
import { LuRedo } from 'react-icons/lu'
import { RxCross2 } from 'react-icons/rx'
import { MdFormatClear } from 'react-icons/md'

import { fileToBase64 } from '../../utils/base64'
import { extensions } from '../../utils/richTextEditor'

const MenuBar = ({ onChange, onRemove }) => {
    const { editor } = useCurrentEditor()
    const timeoutRef = useRef(null)

    useEffect(() => {
        onChange(editor.getJSON())
    }, [])

    const handleContentChange = (editor) => {
        clearTimeout(timeoutRef.current)
        timeoutRef.current = setTimeout(() => {
            if (onChange) {
                console.log(editor.getJSON())
                onChange(editor.getJSON())
            }
        }, 500)
    }

    editor.on('update', ({ editor }) => {
        handleContentChange(editor)
    })
    const fileInputRef = useRef(null)

    if (!editor) {
        return null
    }

    const handleImageUpload = async (event) => {
        console.log('CHANGED')
        const file = event.target.files[0]
        if (!file) return

        const base64Buffer = await fileToBase64(file)
        editor.chain().focus().setImage({ src: base64Buffer }).run()
    }

    return (
        <div className="rich-text-editor-menu-bar">
            <div className="rich-text-editor-menu-bar-buttons">
                <button
                    type="button"
                    title="Bold"
                    onClick={() => editor.chain().focus().toggleBold().run()}
                    disabled={!editor.can().chain().focus().toggleBold().run()}
                    className={
                        editor.isActive('bold')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <FiBold />
                </button>
                <button
                    type="button"
                    title="Italic"
                    onClick={() => editor.chain().focus().toggleItalic().run()}
                    disabled={
                        !editor.can().chain().focus().toggleItalic().run()
                    }
                    className={
                        '' +
                        ' ' +
                        (editor.isActive('italic')
                            ? 'rich-text-editor-button-active'
                            : '')
                    }
                >
                    <FiItalic />
                </button>
                <button
                    type="button"
                    title="Ștergere formatare"
                    onClick={() => editor.chain().focus().unsetAllMarks().run()}
                >
                    <MdFormatClear />
                </button>

                <hr className="rich-text-editor-menu-bar-divider" />

                <button
                    type="button"
                    title="Paragraf"
                    onClick={() => editor.chain().focus().setParagraph().run()}
                    className={
                        '' + ' ' + editor.isActive('paragraph')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <GrTextAlignLeft />
                </button>
                <button
                    type="button"
                    title="Puncte de paragraf"
                    onClick={() =>
                        editor.chain().focus().toggleBulletList().run()
                    }
                    className={
                        '' + ' ' + editor.isActive('bulletList')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <GoListUnordered />
                </button>
                <button
                    type="button"
                    title="Listă ordonată"
                    onClick={() =>
                        editor.chain().focus().toggleOrderedList().run()
                    }
                    className={
                        '' + ' ' + editor.isActive('orderedList')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <GoListOrdered />
                </button>

                <button
                    type="button"
                    title="Rând nou"
                    onClick={() => editor.chain().focus().setHardBreak().run()}
                >
                    <IoIosReturnLeft />
                </button>

                <hr className="rich-text-editor-menu-bar-divider" />

                <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    style={{ display: 'none' }}
                    ref={fileInputRef}
                />
                <button
                    type="button"
                    onClick={() => {
                        fileInputRef.current.click()
                    }}
                >
                    <FiImage />
                </button>

                <button
                    type="button"
                    title="Înapoi"
                    onClick={() => editor.chain().focus().undo().run()}
                    disabled={!editor.can().chain().focus().undo().run()}
                >
                    <LuUndo />
                </button>
                <button
                    type="button"
                    title="Înainte"
                    onClick={() => editor.chain().focus().redo().run()}
                    disabled={!editor.can().chain().focus().redo().run()}
                >
                    <LuRedo />
                </button>
            </div>
            <button type="button" onClick={onRemove}>
                <RxCross2 />
            </button>
        </div>
    )
}

const content = `
<p>
  this is a <em>basic</em> example of <strong>tiptap</strong>.
</p>
`

function RichTextEditor({ onChange, onRemove }) {
    return (
        <div className="rich-text-editor">
            <EditorProvider
                slotBefore={<MenuBar onRemove={onRemove} onChange={onChange} />}
                extensions={extensions}
                content={content}
            ></EditorProvider>
        </div>
    )
}

export default RichTextEditor
