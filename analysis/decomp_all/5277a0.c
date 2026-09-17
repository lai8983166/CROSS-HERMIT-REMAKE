
/* Library Function - Multiple Matches With Different Base Names
    public: void * __thiscall ATL::CStringT<char,class StrTraitMFC<char,class ATL::ChTraitsCRT<char>
   > >::`vector deleting destructor'(unsigned int)
    public: void * __thiscall ATL::CStringT<wchar_t,class StrTraitMFC<wchar_t,class
   ATL::ChTraitsCRT<wchar_t> > >::`vector deleting destructor'(unsigned int)
   
   Library: Visual Studio 2003 Release */

undefined4 * __thiscall FID_conflict__vector_deleting_destructor_(undefined4 *param_1,byte param_2)

{
  undefined4 *puVar1;
  
  if ((param_2 & 2) == 0) {
    thunk_FUN__text__005310c1();
    puVar1 = param_1;
    if ((param_2 & 1) != 0) {
      FUN__text__00428ad0(param_1);
    }
  }
  else {
    puVar1 = param_1 + -1;
    FUN__text__0056de40(param_1,4,*puVar1,thunk_FUN__text__005310c1);
    if ((param_2 & 1) != 0) {
      FUN__text__00428ad0(puVar1);
    }
  }
  return puVar1;
}

