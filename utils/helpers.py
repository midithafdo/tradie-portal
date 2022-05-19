from enum import Enum
from typing import List, Optional, Type

from fastapi import HTTPException, Request


def string_param(
    param_name: str, multi: Optional[bool] = False, enum: Optional[Type[Enum]] = None, default: Optional[str] = None
):
    def parse(request: Request) -> Optional[List[str]]:
        val = request.query_params.get(param_name)
        if val is None:
            return [default] if default is not None else None

        enum_values = set(item.value for item in enum) if enum else None

        if multi is True:
            val = val.split(",")
            if enum_values is not None:
                if any(i not in enum_values for i in val):
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid "{param_name}" query parameter "{val}": must be comma separated values from "{enum_values}"',
                    )
        elif enum_values is not None and val not in enum_values:
            raise HTTPException(
                status_code=400,
                detail=f'Invalid "{param_name}" query parameter "{val}": must be comma separated values from "{enum_values}"',
            )

        if not isinstance(val, list):
            val = [val]

        return val

    return parse
