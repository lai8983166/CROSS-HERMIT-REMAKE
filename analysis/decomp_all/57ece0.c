
/* Library Function - Multiple Matches With Different Base Names
    __set_errno
    __set_errno_from_matherr
   
   Library: Visual Studio */

errno_t __cdecl FID_conflict___set_errno_from_matherr(int _Value)

{
  if (_Value == 1) {
    _Value = FUN__text__00576d20();
    *(undefined4 *)_Value = 0x21;
  }
  else if ((1 < _Value) && (_Value < 4)) {
    _Value = FUN__text__00576d20();
    *(undefined4 *)_Value = 0x22;
  }
  return _Value;
}

