import React from 'react';
import * from './actiontypes';


export const createTag = (tag) => {
    return {
        type: CREATE_TAG,
        payload: doc
    }
}
export const deleteTag = (id) => {
    return {
        type: DELETE_TAG,
        payload: id
    }
}
