
/* WARNING: Instruction at (ram,0x0083db20) overlaps instruction at (ram,0x0083db1f)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Removing unreachable block (ram,0x0083dc68) */
/* WARNING: Removing unreachable block (ram,0x0083db61) */
/* WARNING: Removing unreachable block (ram,0x0083dae0) */
/* WARNING: Removing unreachable block (ram,0x0083db25) */
/* WARNING: Removing unreachable block (ram,0x0083db08) */
/* WARNING: Removing unreachable block (ram,0x0083db24) */
/* WARNING: Removing unreachable block (ram,0x0083dbf7) */
/* WARNING: Removing unreachable block (ram,0x0083dae8) */
/* WARNING: Removing unreachable block (ram,0x0083da93) */
/* WARNING: Removing unreachable block (ram,0x0083da91) */
/* WARNING: Removing unreachable block (ram,0x0083db1f) */
/* WARNING: Removing unreachable block (ram,0x0083dbef) */
/* WARNING: Removing unreachable block (ram,0x0083db18) */
/* WARNING: Removing unreachable block (ram,0x0083dbe9) */
/* WARNING: Removing unreachable block (ram,0x0083daee) */

undefined4 FUN__text1__0083da61(undefined4 param_1,undefined4 param_2,int param_3)

{
  undefined1 *puVar1;
  undefined1 *unaff_EDI;
  undefined1 local_2d8 [716];
  undefined2 local_c;
  undefined1 local_a;
  
  local_c = DAT_0086ed18;
  local_a = DAT_0086ed1a;
  puVar1 = &stack0xfffffffc;
  if (param_3 == 0) {
    _memset(local_2d8,0,0x2cc);
    *(undefined4 *)(unaff_EDI + -0x2d4) = 0x10001;
                    /* WARNING: Bad instruction - Truncating control flow here */
    GetThreadContext(*(HANDLE *)(*(int *)(unaff_EDI + 8) + 4),(LPCONTEXT)(unaff_EDI + -0x2d4));
    *(undefined4 *)(unaff_EDI + 0x10) = *(undefined4 *)(unaff_EDI + -0x21c);
    puVar1 = unaff_EDI;
  }
  if ((*(uint *)(puVar1 + 0xc) & 0xff) == 0) {
    WriteProcessMemory((HANDLE)**(undefined4 **)(puVar1 + 8),*(LPVOID *)(puVar1 + 0x10),
                       &DAT_008752c4,2,(SIZE_T *)(puVar1 + -4));
  }
  else {
    ReadProcessMemory((HANDLE)**(undefined4 **)(puVar1 + 8),*(LPCVOID *)(puVar1 + 0x10),
                      &DAT_008752c4,2,(SIZE_T *)(puVar1 + -4));
    WriteProcessMemory((HANDLE)**(undefined4 **)(puVar1 + 8),*(LPVOID *)(puVar1 + 0x10),puVar1 + -8,
                       2,(SIZE_T *)(puVar1 + -4));
  }
  return 1;
}

