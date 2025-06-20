from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from supabase import create_client, Client

router = APIRouter()

# Initialize Supabase client
supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Supabase URL and service role key must be set in environment variables")

supabase: Client = create_client(supabase_url, supabase_key)

class FAQDeleteResponse(BaseModel):
    success: bool
    error: Optional[str] = None

@router.delete("/{id}", response_model=FAQDeleteResponse)
async def delete_faq(id: str):
    """
    Delete a FAQ by its ID
    """
    try:
        if not id:
            raise HTTPException(status_code=400, detail="FAQ ID is required")

        # First, try to disable RLS for this operation
        try:
            await supabase.rpc("disable_rls")
        except Exception as rls_error:
            print("Could not disable RLS, continuing with service role:", str(rls_error))

        # Delete the FAQ
        response = await supabase.table("faqs").delete().eq("id", id).execute()
        
        if response.error:
            raise HTTPException(status_code=500, detail=response.error.message)

        return FAQDeleteResponse(success=True)

    except HTTPException as he:
        return FAQDeleteResponse(success=False, error=str(he.detail))
    except Exception as e:
        print("Unexpected error:", str(e))
        return FAQDeleteResponse(success=False, error="An unexpected error occurred") 