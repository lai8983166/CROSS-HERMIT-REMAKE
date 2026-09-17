
/* Library Function - Multiple Matches With Different Base Names
    __expand_dbg
    __realloc_dbg
   
   Library: Visual Studio 2003 Debug */

void FID_conflict___realloc_dbg
               (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005f9678;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  ExceptionList = &pvStack_14;
  FUN__text__00577040(9);
  local_8 = 0;
  FUN__text__0056ed90(param_1,param_2,param_3,param_4,param_5,1);
  local_8 = 0xffffffff;
  FUN__text__0056ed63();
  FUN__text__0056ed6e();
  return;
}

