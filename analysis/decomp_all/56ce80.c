
/* Library Function - Single Match
    __chkesp
   
   Library: Visual Studio */

undefined4 __chkesp(void)

{
  code *pcVar1;
  undefined4 in_EAX;
  int iVar2;
  undefined4 uVar3;
  bool in_ZF;
  
  if (in_ZF) {
    return in_EAX;
  }
  iVar2 = FUN_00573780(1,"i386\\chkesp.c",0x2a,&DAT_005953ac,
                       "The value of ESP was not properly saved across a function call.  This is usually a result of calling a function declared with one calling convention with a function pointer declared with a different calling convention. "
                      );
  if (iVar2 == 1) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  return in_EAX;
}

