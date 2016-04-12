import React from 'react';
import * from './actiontypes';

export const createDocument = (doc) => {
    return {
        type: CREATE_DOCUMENT,
        payload: doc
    }
}
export const deleteDocument = (id) => {
    return {
        type: DELETE_DOCUMENT,
        payload: id
    }
}
export const addTagToDocument= (tag, doc) => {
    return {
        type: ADD_TAG_TO_DOCUMENT,
        payload: {
            tag,
            document: doc
        }
    }
}
export const removeTagFromDocument= (tag, doc) => {
    return {
        type: REMOVE_TAG_FROM_DOCUMENT,
        payload: {
            tag,
            document: doc
        }
    }
}
