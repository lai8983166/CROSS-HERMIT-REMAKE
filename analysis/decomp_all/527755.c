
/* Library Function - Single Match
    public: void * __thiscall CODBCFieldInfo::`vector deleting destructor'(unsigned int)
   
   Library: Visual Studio 2003 Release */

void * __thiscall CODBCFieldInfo::_vector_deleting_destructor_(CODBCFieldInfo *this,uint param_1)

{
  CODBCFieldInfo *pCVar1;
  
  if ((param_1 & 2) == 0) {
    thunk_FUN__text__00531052();
    pCVar1 = this;
    if ((param_1 & 1) != 0) {
      FUN__text__00428ad0(this);
    }
  }
  else {
    pCVar1 = this + -4;
    FUN__text__0056de40(this,0x10,*(undefined4 *)pCVar1,thunk_FUN__text__00531052);
    if ((param_1 & 1) != 0) {
      FUN__text__00428ad0(pCVar1);
    }
  }
  return pCVar1;
}

