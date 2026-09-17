
/* Library Function - Single Match
    __ms_p5_mp_test_fdiv
   
   Libraries: Visual Studio 2003, Visual Studio 2005, Visual Studio 2008 */

void __ms_p5_mp_test_fdiv(void)

{
  int iVar1;
  code *pcVar2;
  
  iVar1 = (*DAT_005922c8)("KERNEL32");
  if ((iVar1 != 0) &&
     (pcVar2 = (code *)(*DAT_005922cc)(iVar1,"IsProcessorFeaturePresent"), pcVar2 != (code *)0x0)) {
    (*pcVar2)(0);
    return;
  }
  FUN__text__00573e40();
  return;
}

